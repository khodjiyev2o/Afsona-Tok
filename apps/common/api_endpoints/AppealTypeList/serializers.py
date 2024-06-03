from rest_framework import serializers

from apps.common.models import AppealTypeList


class AppealTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealTypeList
        fields = (
            "name",
        )
