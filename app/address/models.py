from django.db import models

from language.models import Language


class Address(models.Model):

    address = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.address


class AddressGeoData(models.Model):

    address = models.OneToOneField(
        to=Address, on_delete=models.CASCADE, related_name="geo_data")

    continent_code = models.CharField(max_length=5)
    continent_name = models.CharField(max_length=20)

    country_code = models.CharField(max_length=5)
    country_name = models.CharField(max_length=20)

    region_code = models.CharField(max_length=5)
    region_name = models.CharField(max_length=20)

    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)

    latitude = models.FloatField()
    longitude = models.FloatField()

    geoname_id = models.IntegerField()
    capital = models.CharField(max_length=20)

    languages = models.ManyToManyField(
        to=Language, related_name="address_geo_data")

    country_flag = models.CharField(max_length=50)
    country_flag_emoji = models.CharField(max_length=50)
    country_flag_emoji_unicode = models.CharField(max_length=50)

    calling_code = models.CharField(max_length=5)
    is_eu = models.BooleanField()

    def __str__(self):
        return f"{self.address} geo data"
