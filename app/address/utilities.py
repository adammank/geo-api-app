from .constants import ACCESS_KEY
from .serializers import (AddressSerializer,
                          AddressGeoDataSerializer)


def geo_api_link(address):
    return f"http://api.ipstack.com/{address}?" \
           f"access_key={ACCESS_KEY}&format=1"


def serialize_address(data: dict):
    """ Check if the given address data is valid.
        If yes, return address value.
        If not, raise an exception."""

    serializer = AddressSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data.get('address')


def get_or_create_address(ip: str):
    """ Check if the given address value is valid.
        If yes, create and/or get the Address object.
        If not, raise an exception. """

    serializer = AddressSerializer(data={"address": ip})
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def get_or_create_address_geo_data(data: dict):
    """ Check if the given data is valid.
        If yes, create and get the GeoData object.
        If not or the object already exists, raise an exception. """

    serializer = AddressGeoDataSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer