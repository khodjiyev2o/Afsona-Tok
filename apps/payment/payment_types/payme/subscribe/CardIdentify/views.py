from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.payment.payment_types.payme.subscribe.CardIdentify.serializers import CardIdentifySerializer
from utils.card_identifier import CARDS


class CardIdentifyView(GenericAPIView):
    serializer_class = CardIdentifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            card_number = serializer.validated_data.get('digits')
            for card_type in CARDS['data']['cardTypes']:
                for system_card in card_type['ranges']:
                    if card_number in system_card['start'] or card_number in system_card['end']:
                        return Response({"source": card_type["processing"], "vendor": card_type['vendor']})
            raise ValidationError(detail="Card Number is not supported", code="invalid_card_number")


__all__ = ['CardIdentifyView']
