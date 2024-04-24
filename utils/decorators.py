import functools

from requests import request
from requests.exceptions import Timeout
from requests.exceptions import RequestException

from rest_framework.serializers import ValidationError


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
            response.raise_for_status()
        except (Timeout, RequestException) as error:
            raise ValidationError(detail={"payme": "Timeout Exception"}, code=f"timeout")
        return response.json()

    return wrapper
