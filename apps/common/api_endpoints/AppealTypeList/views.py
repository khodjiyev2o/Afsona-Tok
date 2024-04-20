from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.models import AppealTypeList
from apps.common.api_endpoints.AppealTypeList.serializers import AppealTypeListSerializer


class AppealTypeListView(generics.ListAPIView):
    queryset = AppealTypeList.objects.all()
    serializer_class = AppealTypeListSerializer
    permission_classes = [IsAuthenticated]


__all__ = ['AppealTypeListView']
