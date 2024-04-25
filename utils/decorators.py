import functools
import json

from requests import request
from requests.exceptions import Timeout
from requests.exceptions import RequestException

from rest_framework.serializers import ValidationError

from apps.payment.models import MerchantRequestLog, Transaction


def payme_request(func):
    """
    Payme request decorator.
    """
    @functools.wraps(func)
    def wrapper(self, data):
        response = None
        req_data = {
            "method": "POST",
            "url": self.base_url,
            "data": data,
            "headers": self.headers,
            "timeout": self.timeout,
        }
        try:
            response = request(**req_data)
            data_dict = json.loads(req_data['data'])

            MerchantRequestLog.objects.create(
                payment_type=Transaction.PaymentType.PAYME,
                method_type=data_dict['method'],
                request_headers=self.headers,
                request_body=req_data,
                response_status_code=response.status_code,
                response_body=response.json(),
            )
            response.raise_for_status()
        except (Timeout, RequestException) as error:
            raise ValidationError(detail={"payme": "Timeout Exception"}, code=f"timeout")
        return response.json()

    return wrapper
