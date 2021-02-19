from django.core.management.base import BaseCommand
from django.db import transaction

from ..command_constants import LANGUAGES, ADDRESSES, GEO_DATA
from ...models import Address, AddressGeoData
from ...serializers import AddressGeoDataSerializer
from language.models import Language


class Command(BaseCommand):
    help = "Creates the initial data."

    @transaction.atomic()
    def handle(self, *args, **options):
        self._create_language_objects()
        self._create_address_objects()
        self._create_address_geo_data_objects()

    @staticmethod
    def _create_language_objects():
        for index, language in enumerate(LANGUAGES, start=1):
            try:
                Language.objects.get(name=language)
                print(f'\tLanguage{index} is already present in the db.')
            except Language.DoesNotExist:
                Language.objects.create(name=language)
                print(f'\tLanguage{index} created.')

    @staticmethod
    def _create_address_objects():
        for index, address in enumerate(ADDRESSES, start=1):
            try:
                Address.objects.get(address=address)
                print(f'\tAddress{index} is already present in the db.')
            except Address.DoesNotExist:
                Address.objects.create(address=address)
                print(f'\tAddress{index} created.')

    @staticmethod
    def _create_address_geo_data_objects():
        for index, data in enumerate(GEO_DATA, start=1):
            try:
                AddressGeoData.objects.get(address__address=data.get('address'))
                print(f'\tGeoData{index} is already present in the db.')
            except AddressGeoData.DoesNotExist:
                serializer = AddressGeoDataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    print(f'\tAddress{index} geo data created.')
