from rest_framework import serializers

from apps.common.models import StaticPage


class ListStaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ("id", "title")


class DetailStaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ("id", "title", "content")

