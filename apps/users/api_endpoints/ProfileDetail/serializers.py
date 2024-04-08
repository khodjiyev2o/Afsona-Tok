from rest_framework import serializers
from apps.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo", "phone", "balance", "date_of_birth", "language")
