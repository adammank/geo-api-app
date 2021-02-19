from rest_framework import serializers

from .models import Language


class LanguageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15, required=True)

    def create(self, validated_data):
        language_obj, created = Language.objects.get_or_create(
            name=validated_data['name'])
        return language_obj
