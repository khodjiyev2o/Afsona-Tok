from rest_framework import generics, status
from rest_framework.response import Response

from apps.common.models import SavedLocation
from apps.common.api_endpoints.SavedLocation.serializers import SavedLocationSerializer


class SavedLocationAPIView(generics.CreateAPIView):
    queryset = SavedLocation.objects.all()
    serializer_class = SavedLocationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance, created = self.queryset.get_or_create(
            user=self.request.user, location=serializer.validated_data['location'],
            defaults={'location': serializer.validated_data['location'], 'user': self.request.user}
        )
        if not created: instance.delete() # noqa

        status_code = {True: status.HTTP_201_CREATED, False: status.HTTP_204_NO_CONTENT}
        return Response(data=serializer.data, status=status_code[created])


__all__ = ['SavedLocationAPIView']
