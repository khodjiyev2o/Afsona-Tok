from typing import Union
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.providers.payme_merchant.auth import PaymeBasicAuthentication
from apps.payment.providers.payme_merchant import status_codes
from apps.payment.providers.payme_merchant.serializers import PaymeCallbackSerializer
import sentry_sdk
from apps.payment.models import Transaction as PaymentTransaction
from django.conf import settings


class PaymeCallbackView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.METHOD_MAPPING = {
            "CreateTransaction": self._create_transaction,
            "CheckPerformTransaction": self._check_perform_transaction,
            "PerformTransaction": self._perform_transaction,
            "CheckTransaction": self._check_transaction,
            "CancelTransaction": self._cancel_transaction,
            "GetStatement": None,
            "SetFiscalData": None
        }
        self.credential_key = settings.PAYMENTS_CREDENTIALS['payme']['credential_key']

    authentication_classes = (PaymeBasicAuthentication,)  # todo should use custom exception for 'AUTH_MESSAGE'
    permission_classes = (AllowAny,)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, args, kwargs)
        except Exception as ex:  # should be pass all Exception
            sentry_sdk.capture_exception(ex)
            return Response(data=status_codes.INTERNAL_SERVER_ERROR_MESSAGE)

    def post(self, request, *args, **kwargs):

        if not request.user:
            return Response(data=status_codes.AUTH_MESSAGE)

        serializer = PaymeCallbackSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=status_codes.PARSING_JSON_MESSAGE)

        method = serializer.validated_data['method']
        if method not in self.METHOD_MAPPING:
            return Response(data=status_codes.RPC_METHOD_NOT_FOUND_MESSAGE)

        if not callable(self.METHOD_MAPPING.get(method)):
            return Response(data=status_codes.RPC_METHOD_NOT_IMPLEMENT_MESSAGE)

    @classmethod
    def _check_perform_transaction(cls, params: dict, credential_key: str) -> dict:
        params_transaction_id = int(params.get('account', {}).get(credential_key, 0))
        params_amount = params.get('amount')

        transaction = cls.__get_transaction(pk=params_transaction_id)

        if transaction is None:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE

        if transaction.amount != params_amount / 100:
            return status_codes.INVALID_AMOUNT_MESSAGE

        if transaction.status == PaymentTransaction.StatusType.ACCEPTED:
            return status_codes.ORDER_ALREADY_PAID_MESSAGE

        if transaction.status != PaymentTransaction.StatusType.PENDING:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE

        return {"result": {"allow": True}, "additional": {"user_id": transaction.user_id}}

    @classmethod
    def _create_transaction(cls, params: dict, credential_key: str) -> dict:
        params_transaction_id = int(params.get('account', {}).get(credential_key, 0))
        params_amount = params.get('amount')

        transaction = cls.__get_transaction(pk=params_transaction_id)
        if transaction is None:
            return status_codes.ORDER_NOT_FOUND_MESSAGE

        if transaction.status == PaymentTransaction.StatusType.ACCEPTED:
            return status_codes.ORDER_ALREADY_PAID_MESSAGE

        if transaction.status != PaymentTransaction.StatusType.PENDING:
            return status_codes.ORDER_NOT_FOUND_MESSAGE

        if transaction.amount != params_amount / 100:
            return status_codes.INVALID_AMOUNT_MESSAGE

        transaction.remote_id = params.get('id')
        transaction.save(update_fields=['remote_id'])

        return {
            "result": {
                "create_time": timezone.now().timestamp() * 1000,
                "transaction": transaction.remote_id,
                "state": status_codes.TransactionStates.CREATED,
            }
        }

    @classmethod
    def _perform_transaction(cls, params: dict, **kwargs):
        params_transaction_id = params.get('id')

        transaction = cls.__get_transaction(remote_id=params_transaction_id)
        if transaction is None:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE
        if transaction.status == PaymentTransaction.StatusType.REJECTED:
            return status_codes.UNABLE_TO_PERFORM_OPERATION_MESSAGE

        if transaction.status == PaymentTransaction.StatusType.ACCEPTED:
            return status_codes.ORDER_ALREADY_PAID_MESSAGE


    @classmethod
    def _check_transaction(cls):
        return

    @classmethod
    def _cancel_transaction(cls):
        return

    @staticmethod
    def __get_transaction(**kwargs) -> Union[PaymentTransaction | None]:
        transaction = PaymentTransaction.objects.filter(**kwargs).first()
        return transaction
