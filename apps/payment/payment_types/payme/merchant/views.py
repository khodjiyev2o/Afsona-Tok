import json
from typing import Union
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.payment_types.payme.merchant.auth import PaymeBasicAuthentication
from apps.payment.payment_types.payme.merchant import status_codes
from apps.payment.payment_types.payme.merchant.serializers import PaymeCallbackSerializer
import sentry_sdk
from apps.payment.models import Transaction as PaymentTransaction, MerchantRequestLog
from django.conf import settings


class PaymeCallbackView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            response = super().dispatch(request, *args, **kwargs)
            merchant_log = MerchantRequestLog.objects.create(
                payment_type=PaymentTransaction.PaymentType.PAYME,
                request_headers=self.request.headers,
                request_body=self.request.data,
                response_headers=response.headers,
                response_status_code = response.status_code,
                response_body = response.data,
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

        # todo should minus transaction amount from user balance if reason is 5

        return {
            "result": {
                "transaction": transaction.remote_id,
                "cancel_time": transaction.canceled_at.timestamp() * 1000 if transaction.canceled_at else 0,
                "state": cls.__get_transaction_state(transaction),
            }
        }

    @staticmethod
    def __get_transaction(**kwargs) -> Union[PaymentTransaction | None]:
        transaction = PaymentTransaction.objects.filter(
            payment_type=PaymentTransaction.PaymentType.PAYME, **kwargs,
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

        if state == status_codes.TransactionStates.CLOSED and transaction.paid_at is None:
            state = status_codes.TransactionStates.CANCELED_CLOSED

        return state
