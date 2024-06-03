from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.payment.models import UserCard
from .serializers import UserCardVerifySerializer


class UserCardVerifyAPIView(CreateAPIView):
    serializer_class = UserCardVerifySerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_card = UserCard.objects.filter(user=request.user, cid=serializer.validated_data["token"]).first()
        # Send request to CONFIRM create card
        response = serializer.verify_card(user_card=user_card)
        return Response(data=response, status=status.HTTP_200_OK)


__all__ = ["UserCardVerifyAPIView"]
