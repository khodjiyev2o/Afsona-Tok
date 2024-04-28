from rest_framework import serializers

from apps.users.models import User


class ProfileUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ("full_name", "date_of_birth", "photo", "language", "phone", "balance")
