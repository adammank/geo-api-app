from django.contrib import admin

from .models import Address, AddressGeoData


admin.site.register(Address)
admin.site.register(AddressGeoData)