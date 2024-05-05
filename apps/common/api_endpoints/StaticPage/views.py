from rest_framework import generics
from apps.common.models import StaticPage
from apps.common.api_endpoints.StaticPage import serializers


class ListStaticPageAPIView(generics.ListAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = serializers.ListStaticPageSerializer
    permission_classes = []


class DetailStaticPageAPIView(generics.RetrieveAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = serializers.DetailStaticPageSerializer
    permission_classes = []


__all__ = ['ListStaticPageAPIView', 'DetailStaticPageAPIView']
