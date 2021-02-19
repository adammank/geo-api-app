from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from language.models import Language
from .models import Address, AddressGeoData


class AddressGeoDataSerializer(serializers.ModelSerializer):

    address = serializers.SlugRelatedField(
        slug_field='address', queryset=Address.objects.all(), required=True)

    languages = serializers.SlugRelatedField(
        slug_field='name', queryset=Language.objects.all(), many=True)

    class Meta:
        model = AddressGeoData
        exclude = ('id', )

    def validate_address(self, value):
        if AddressGeoData.objects.filter(address__address=value):
            raise ValidationError("This address already exists.")
        return value


class AddressModelSerializer(serializers.ModelSerializer):
    geo_data = AddressGeoDataSerializer(read_only=True)

    class Meta:
        model = Address
        fields = ('address', 'geo_data')


class AddressSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=30, required=True)

    def create(self, validated_data):
        address_obj, created = Address.objects.get_or_create(
            address=validated_data['address'])
        return address_obj
