from rest_framework import serializers

from apps.users.models import User


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("full_name", "date_of_birth", "photo", "language")
