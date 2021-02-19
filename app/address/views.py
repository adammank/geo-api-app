from rest_framework import status, generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction
from django.shortcuts import get_object_or_404

from language.utilities import get_or_create_languages
from .models import Address, AddressGeoData
from .serializers import AddressModelSerializer, AddressGeoDataSerializer
from .service import GeoDataService
from .utilities import (serialize_address, get_or_create_address,
                        get_or_create_address_geo_data)


class AddressGeoDataAddView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        # validate the address & return the value
        address = serialize_address(data=request.data)

        # get the geo-data based on the passed address
        data = GeoDataService(address=address).get_data()
        if not data:
            return Response(
                data={"error": "unknown address"},
                status=status.HTTP_404_NOT_FOUND)

        # get or create the Address object
        address_obj = get_or_create_address(ip=data.get('ip'))
        data['address'] = address_obj.address

        # get or create the Language objects
        languages = [language.get('name') for language
                     in data.get('languages')]
        language_objs = get_or_create_languages(languages=languages)
        data['languages'] = language_objs

        # get or create the final AddressGeoData object
        address_geo_data_obj = get_or_create_address_geo_data(data=data)
        return Response(data=address_geo_data_obj.data,
                        status=status.HTTP_201_CREATED)


class AddressGeoDataDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):

        # validate the address & return the value
        address = serialize_address(data=request.data)

        # if the passed address is an IP present in the db
        geo_data_objs = AddressGeoData.objects.filter(address__address=address)
        if geo_data_objs.count() == 1:
            geo_data_objs.get().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # other cases (f.g: address was passed as an url or hostname)
        data = GeoDataService(address=address).get_data()
        if not data:
            return Response(
                data={"error": "unknown address"},
                status=status.HTTP_404_NOT_FOUND)

        geo_data_obj = get_object_or_404(
            AddressGeoData, address__address=data.get('ip'))
        geo_data_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressGeoDataProvideView(generics.CreateAPIView):
    queryset = AddressGeoData.objects.all()
    serializer_class = AddressGeoDataSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # validate the address & return the value
        address = serialize_address(
            data={'address': request.data.get('address')})

        # get or create the Language objects
        language_objs = get_or_create_languages(
            languages=request.data.get('languages'))
        request.data['languages'] = language_objs

        # if the passed address is an IP present in the db
        address_obj = Address.objects.filter(address=address)
        if address_obj.count() == 1:
            return self.create(request)

        # other cases (f.g: address was passed as an url or hostname)
        data = GeoDataService(address=address).get_data()
        if not data:
            return Response(
                data={"error": "unknown address"},
                status=status.HTTP_404_NOT_FOUND)

        address_obj = get_object_or_404(
            Address, address=data.get('ip'))
        request.data['address'] = address_obj.address

        return self.create(request)


class AddressListView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressModelSerializer
    permission_classes = [IsAuthenticated]
