from rest_framework import generics

from apps.chargers.models import Connector
from apps.chargers.api_endpoints.ConnectorDetail.serializers import ConnectorDetailSerializer


class ConnectorDetailView(generics.RetrieveAPIView):
    """List of connection types"""
    serializer_class = ConnectorDetailSerializer
    queryset = Connector.objects.all()


__all__ = ['ConnectorDetailView']
