from rest_framework import generics
from apps.common.models import ConnectionType

from apps.common.api_endpoints.ConnectionTypeList.serializers import ConnectionTypeListSerializer


class ConnectionTypeListView(generics.ListAPIView):
    """List of connection types"""
    serializer_class = ConnectionTypeListSerializer
    queryset = ConnectionType.objects.all()
    filterset_fields = ("_type",)


__all__ = ['ConnectionTypeListView']
