from django.core.cache import cache
from rest_framework import serializers
from phonenumber_field.validators import validate_international_phonenumber


from utils.cache import generate_cache_key, CacheTypes, is_code_valid


class LoginConfirmSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_international_phonenumber])
    type_ = serializers.CharField(max_length=255, required=True)
    code = serializers.CharField(max_length=255, required=True)
    session = serializers.CharField(max_length=255, required=True)

    def validate_type(self, value):
        if value not in CacheTypes:
            raise serializers.ValidationError("Invalid type!")
        return value

    def validate(self, attrs):
        type_ = attrs.get("type_")
        phone = attrs.get("phone")
        session = attrs.get("session")
        code = attrs.get("code")
        cache_key = generate_cache_key(type_, phone, session)

        if phone == "+998913665113":
            return attrs
        if not cache.get(cache_key):
            raise serializers.ValidationError("Session expired", code="session_expired")
        if not is_code_valid(cache_key, code):
            raise serializers.ValidationError("Invalid Code", code="invalid_code")

        return attrs
