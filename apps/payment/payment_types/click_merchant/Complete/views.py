from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from apps.common.models import MainSettings
from apps.payment.payment_types.click_merchant.Complete.serializers import \
    ClickCompleteSerializer

from apps.payment.models import Transaction
from apps.payment.payment_types.click_merchant.auth import authentication
from apps.payment.payment_types.click_merchant.provider import ClickProvider
from apps.payment.payment_types.click_merchant.views import PaymentView


class ClickCompleteAPIView(PaymentView):
    TYPE = "complete"
    PROVIDER = Transaction.PaymentType.CLICK  # type: ignore
    permission_classes = []

    @swagger_auto_schema(request_body=ClickCompleteSerializer)
    def post(self, request, *args, **kwargs):
        check_auth = authentication(request)
        if not check_auth:
            return Response({"error": "-1", "error_note": _("SIGN CHECK FAILED!")})

        serializer = ClickCompleteSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            click_provider = ClickProvider(serializer.validated_data)
            response = click_provider.complete()

        response["fiscal_items"] = list()

        if click_provider.has_transaction:
            transaction = click_provider.transaction
        else:
            transaction = None

        response["click_trans_id"] = serializer.validated_data.get("click_trans_id", None)
        response["merchant_trans_id"] = serializer.validated_data.get("merchant_trans_id", None)
        response["merchant_prepare_id"] = serializer.validated_data.get("merchant_prepare_id", None)
        response["merchant_confirm_id"] = serializer.validated_data.get("merchant_prepare_id", None)

        if response["error"] == "0":
            transaction = click_provider.transaction

            with db_transaction.atomic():
                transaction.success_process()
                # self.add_fiscal_data(response, transaction)
            return Response(response)

        if transaction and transaction.status == Transaction.StatusType.PENDING:
            transaction.status = Transaction.StatusType.CANCELED
            transaction.save()

        return Response(response)

    @staticmethod
    def add_fiscal_data(response, transaction):
        response["received_cash"] = 0
        response["received_ecash"] = 0
        response["received_card"] = transaction.amount * 100

        product_name = str(transaction.id)
        sett = MainSettings.objects.last()
        response["fiscal_items"].append(
            {
                "Name": product_name,
                "SPIC": str(sett.soliq_spic),
                "GoodPrice": transaction.amount * 100,
                "Units": 1,
                "Amount": 1,
                "code": str(sett.soliq_service_code),
                "PackageCode": str(sett.soliq_package_code),
                "VAT": transaction.amount * sett.soliq_nds,
                "VATPercent": sett.soliq_nds,
                "CommissionInfo": {"TIN": str(sett.soliq_inn)},
            }
        )


__all__ = ['ClickCompleteAPIView']
