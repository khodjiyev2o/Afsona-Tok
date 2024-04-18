from rest_framework import generics

from apps.common.api_endpoints.InstructionList.serializers import InstructionListSerializer
from apps.common.models import Instruction


class InstructionListAPIView(generics.ListAPIView):
    serializer_class = InstructionListSerializer
    queryset = Instruction.objects.all()


__all__ = ['InstructionListAPIView']
