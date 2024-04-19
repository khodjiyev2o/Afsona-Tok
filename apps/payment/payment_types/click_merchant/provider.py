from decimal import Decimal

from django.utils.translation import gettext_lazy as _

from apps.payment.models import Transaction


class ClickProvider:
    def __init__(self, data):
        self.data = data
        self.click_trans_id = self.data.get("click_trans_id", None)
        self.service_id = self.data.get("service_id", None)
        self.click_paydoc_id = self.data.get("click_paydoc_id", None)
        self.order_id = self.data.get("merchant_trans_id", None)
        self.amount = self.data.get("amount", None)
        self.action = self.data.get("action", None)
        self.error = self.data.get("error", None)
        self.error_note = self.data.get("error_note", None)
        self.sign_time = self.data.get("sign_time", None)
        self.sign_string = self.data.get("sign_string", None)
        self.merchant_prepare_id = self.data.get("merchant_prepare_id", None) if self.action == 1 else ""
        self.order = self.get_order()
        self.success_response = {"error": "0", "error_note": "Success"}
        self.transaction_found = False
        self.transaction = None

    def prepare(self):
        if self.action != 0:
            return {"error": "-3", "error_note": _("Action not found")}

        if not self.order:
            return {"error": "-5", "error_note": _("Order does not exist")}

        check_order, error_response = self.check_order()
        if not check_order:
            return error_response

        # check transaction exist and create if not exist
        can_prepare_transaction, error_response = self.can_prepare_transaction()
        if not can_prepare_transaction:
            return error_response

        # check amount when can_prepare_transaction is True
        is_valid_amount, error_response = self.is_valid_amount()
        if not is_valid_amount:
            return error_response

        return self.success_response

    def complete(self):
        if self.action != 1:
            return {"error": "-3", "error_note": _("Action not found")}

        if not self.order:
            return {"error": "-5", "error_note": _("Order does not exist")}

        check_order, error_response = self.check_order()
        if not check_order:
            return error_response

        can_complete_transaction, error_response = self.can_complete_transaction()
        if not can_complete_transaction:
            return error_response

        # check amount when can_prepare_transaction is True
        is_valid_amount, error_response = self.is_valid_amount()
        if not is_valid_amount:
            return error_response

        return self.success_response

    def can_complete_transaction(self):
        try:
            transaction = Transaction.objects.get(id=self.merchant_prepare_id)
            # set transaction and transaction_found if transaction exist
            self.transaction_found = True
            self.transaction = transaction
            if transaction.remote_id != str(self.click_trans_id):
                return False, {"error": "-8", "error_note": _("Transaction ID not match")}
        except Transaction.DoesNotExist:
            return False, {"error": "-7", "error_note": _("Transaction not found")}

        is_valid_status, error_response = self.check_transaction_status()
        if not is_valid_status:
            return False, error_response

        return True, self.success_response

    def can_prepare_transaction(self):
        transaction = self.get_transaction()
        self.transaction_found = True
        self.transaction = transaction

        is_valid_status, error_response = self.check_transaction_status()
        if not is_valid_status:
            return False, error_response

        return True, self.success_response

    def check_transaction_status(self):
        if self.transaction.status == Transaction.StatusType.ACCEPTED:
            return False, {"error": "-4", "error_note": _("Already paid")}
        elif self.transaction.status in [Transaction.StatusType.CANCELED, Transaction.StatusType.REJECTED]:
            return False, {"error": "-9", "error_note": _("Transaction cancelled or failed")}
        return True, self.success_response

    def get_transaction(self):
        transaction, created = Transaction.objects.get_or_create(
            id=self.order_id,
            payment_type=Transaction.PaymentType.CLICK,
            defaults={"amount": self.amount,
                      "status": Transaction.StatusType.PENDING,
                      }
        )
        transaction.remote_id = self.click_trans_id
        transaction.save(update_fields=['remote_id'])
        return transaction

    @property
    def has_transaction(self):
        return self.transaction_found

    def is_valid_amount(self):
        transaction = Transaction.objects.get(
            id=self.order_id, payment_type=Transaction.PaymentType.CLICK
        )
        if self.amount != transaction.amount + (transaction.amount * Decimal('0.01')):  # 0.01 is the charging fee 1%
            return False, {"error": "-2", "error_note": _("Incorrect parameter amount")}

        return True, self.success_response

    def get_order(self):
        try:
            return Transaction.objects.get(id=self.order_id)
        except Transaction.DoesNotExist:
            return

    def check_order(self):
        if self.order.status == Transaction.StatusType.ACCEPTED:
            return False, {"error": "-4", "error_note": _("Already paid")}
        return True, self.success_response
