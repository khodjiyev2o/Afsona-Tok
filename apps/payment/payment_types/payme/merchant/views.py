from datetime import datetime
from typing import Union

import sentry_sdk
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.models import Transaction as PaymentTransaction, MerchantRequestLog
from apps.payment.payment_types.payme.merchant import status_codes
from apps.payment.payment_types.payme.merchant.auth import PaymeBasicAuthentication
from apps.payment.payment_types.payme.merchant.serializers import PaymeCallbackSerializer


class PaymeCallbackView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.METHOD_MAPPING = {
            "CreateTransaction": self._create_transaction,
            "CheckPerformTransaction": self._check_perform_transaction,
            "PerformTransaction": self._perform_transaction,
            "CheckTransaction": self._check_transaction,
            "CancelTransaction": self._cancel_transaction,
            "GetStatement": self._get_statement,
            "SetFiscalData": None
        }
        self.credential_key = settings.PAYMENT_CREDENTIALS['payme']['credential_key']

    authentication_classes = (PaymeBasicAuthentication,)  # todo should use custom exception for 'AUTH_MESSAGE'
    permission_classes = (AllowAny,)

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
            MerchantRequestLog.objects.create(
                payment_type=PaymentTransaction.PaymentType.PAYME,
                method_type=self.request.data.get('method', None),
                request_headers=self.request.headers,
                request_body=self.request.data,
                response_status_code=response.status_code,
                response_body=response.data,
            )

            return response
        except Exception as ex:  # should be pass all Exception
            sentry_sdk.capture_exception(ex)
            return Response(data=status_codes.INTERNAL_SERVER_ERROR_MESSAGE)

    def post(self, request, *args, **kwargs):

        if not request.user:
            return Response(status_codes.AUTH_MESSAGE)

        serializer = PaymeCallbackSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status_codes.PARSING_JSON_MESSAGE)

        method = serializer.validated_data['method']
        if method not in self.METHOD_MAPPING:
            return Response(status_codes.RPC_METHOD_NOT_FOUND_MESSAGE)

        method_callback_function = self.METHOD_MAPPING.get(method)

        if not callable(method_callback_function):
            return Response(status_codes.RPC_METHOD_NOT_IMPLEMENT_MESSAGE)

        pre_response = method_callback_function(
            params=serializer.validated_data['params'],
            credential_key=self.credential_key
        )

        if "error" in pre_response:
            pass  # log to error

        return Response(pre_response, status=status.HTTP_200_OK)

    @classmethod
    def _check_perform_transaction(cls, params: dict, credential_key: str) -> dict:
        params_transaction_id = int(params.get('account', {}).get(credential_key, 0))
        params_amount = params.get('amount')

        transaction = cls.__get_transaction(pk=int(params_transaction_id))

        if transaction is None:
            return status_codes.ORDER_NOT_FOUND_MESSAGE

        if transaction.amount != params_amount / 100:
            return status_codes.INVALID_AMOUNT_MESSAGE

        if transaction.status == PaymentTransaction.StatusType.ACCEPTED:
            return status_codes.ORDER_ALREADY_PAID_MESSAGE

        if transaction.status != PaymentTransaction.StatusType.PENDING:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE

        return {"result": {"allow": True}, "additional": {"user_id": transaction.user_id}}

    @classmethod
    def _create_transaction(cls, params: dict, credential_key: str) -> dict:
        params_transaction_id = params.get('id', '0')
        params_order_id = int(params.get('account', {}).get(credential_key, 0))
        params_amount = params.get('amount')

        transaction = cls.__get_transaction(pk=params_order_id)
        if transaction is None:
            return status_codes.ORDER_NOT_FOUND_MESSAGE

        if transaction.amount != (params_amount / 100):
            return status_codes.INVALID_AMOUNT_MESSAGE

        if not transaction.remote_id:
            transaction.remote_id = params_transaction_id

        if transaction.remote_id != params_transaction_id:
            return status_codes.ORDER_NOT_FOUND_MESSAGE

        if transaction.status != PaymentTransaction.StatusType.PENDING:
            return status_codes.ORDER_NOT_FOUND_MESSAGE
        transaction.save(update_fields=['remote_id'])
        return {
            "result": {
                "create_time": transaction.created_at.timestamp() * 1000,
                "transaction": transaction.remote_id,
                "state": cls.__get_transaction_state(transaction),
            }
        }

    @classmethod
    def _perform_transaction(cls, params: dict, **kwargs):
        params_transaction_id = params.get('id')

        transaction = cls.__get_transaction(remote_id=params_transaction_id)
        if transaction is None:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE

        if transaction.status == PaymentTransaction.StatusType.ACCEPTED:
            return {"result": {
                "transaction": transaction.remote_id,
                "perform_time": transaction.paid_at.timestamp() * 1000 if transaction.paid_at else 0,
                "state": status_codes.TransactionStates.CLOSED
            }}

        if transaction.status == PaymentTransaction.StatusType.REJECTED:
            return status_codes.UNABLE_TO_PERFORM_OPERATION_MESSAGE

        transaction.status = PaymentTransaction.StatusType.ACCEPTED
        transaction.paid_at = timezone.now()
        transaction.save(update_fields=['status', 'paid_at'])
        transaction.success_process()

        return {"result": {
            "transaction": transaction.remote_id,
            "perform_time": transaction.paid_at.timestamp() * 1000 if transaction.paid_at else 0,
            "state": status_codes.TransactionStates.CLOSED
        }}

    @classmethod
    def _check_transaction(cls, params, **kwargs):
        params_transaction_id = params.get('id')
        transaction = cls.__get_transaction(remote_id=params_transaction_id)

        if not transaction:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE
        return {
            "result": {
                "create_time": transaction.created_at.timestamp() * 1000,
                "perform_time": transaction.paid_at.timestamp() * 1000 if transaction.paid_at else 0,
                "cancel_time": transaction.canceled_at.timestamp() * 1000 if transaction.canceled_at else 0,
                "transaction": transaction.remote_id,
                "state": cls.__get_transaction_state(transaction),
                "reason": transaction.extra.get("payme_cancel_reason") if transaction.extra else None
            }
        }

    @classmethod
    def _cancel_transaction(cls, params, **kwargs) -> dict:
        params_transaction_id = params.get('id', '0')
        reason = params.get('reason')

        transaction = cls.__get_transaction(remote_id=params_transaction_id)
        if not transaction:
            return status_codes.TRANSACTION_NOT_FOUND_MESSAGE

        if transaction.status == PaymentTransaction.StatusType.CANCELED:
            return {
                "result": {
                    "transaction": transaction.remote_id,
                    "cancel_time": transaction.canceled_at.timestamp() * 1000 if transaction.canceled_at else 0,
                    "state": cls.__get_transaction_state(transaction)
                }
            }

        transaction.canceled_at = timezone.now()
        transaction.status = PaymentTransaction.StatusType.CANCELED
        transaction.extra = {"payme_cancel_reason": reason}
        transaction.save(update_fields=['canceled_at', 'status', 'extra'])

        if reason == 5:
            transaction.cancel_process()

        return {
            "result": {
                "transaction": transaction.remote_id,
                "cancel_time": transaction.canceled_at.timestamp() * 1000 if transaction.canceled_at else 0,
                "state": cls.__get_transaction_state(transaction),
            }
        }

    @classmethod
    def _get_statement(cls, params, credential_key: str) -> dict:
        transactions_list: list[dict] = []
        params_from_datetime = datetime.fromtimestamp(params['from'] // 1000)
        params_to_datetime = datetime.fromtimestamp(params['to'] // 1000)

        queryset = PaymentTransaction.objects.filter(
            created_at__gte=params_from_datetime, created_at__lte=params_to_datetime,
            payment_type=PaymentTransaction.PaymentType.PAYME,
            remote_id__isnull=False
        )

        for transaction in queryset:
            transactions_list.append(
                {
                    "id": transaction.remote_id,
                    "amount": transaction.amount,
                    "perform_time": transaction.paid_at.timestamp() * 1000 if transaction.paid_at else 0,
                    "cancel_time": transaction.canceled_at.timestamp() * 1000 if transaction.canceled_at else 0,
                    "create_time": transaction.created_at.timestamp() * 1000,
                    "state": cls.__get_transaction_state(transaction),
                    "reason": transaction.extra.get("payme_cancel_reason") if transaction.extra else None,
                    "account": {
                        credential_key: transaction.id
                    }
                }
            )

        return {"result": {"transactions": transactions_list}}

    @staticmethod
    def __get_transaction(**kwargs) -> Union[PaymentTransaction | None]:
        transaction = PaymentTransaction.objects.filter(
            payment_type__in=[PaymentTransaction.PaymentType.PAYME, PaymentTransaction.PaymentType.CARD], **kwargs,
        ).last()

        return transaction

    @classmethod
    def __get_transaction_state(cls, transaction: PaymentTransaction) -> int:
        transaction_state_mapping = {
            PaymentTransaction.StatusType.PENDING.value: status_codes.TransactionStates.CREATED,
            PaymentTransaction.StatusType.ACCEPTED.value: status_codes.TransactionStates.CLOSED,
            PaymentTransaction.StatusType.CANCELED.value: status_codes.TransactionStates.CANCELED_CREATED,
        }

        state = transaction_state_mapping.get(transaction.status)

        if state == status_codes.TransactionStates.CANCELED_CREATED and transaction.paid_at:
            state = status_codes.TransactionStates.CANCELED_CLOSED

        return state
