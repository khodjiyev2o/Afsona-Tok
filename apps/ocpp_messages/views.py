from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ocpp.v16.enums import RegistrationStatus


def default_index(request):
    return Response(status=200)


class BootNotificationApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        return Response({"interval": 10, "status": RegistrationStatus.accepted}, status=200)


class StatusNotificationApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=200)


class HeartbeatApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=200)


class MeterValuesApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=200)


class StartTransactionApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        return Response({
            "transaction_id": 1,
            "id_tag_info": {
                "status": RegistrationStatus.accepted,
                "id_tag": "random_string_len_20",
                "expiry_date": None  # iso format
            }
        }, status=200)


class StopTransactionApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(status=200)
