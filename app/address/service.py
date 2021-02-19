import requests
from .utilities import geo_api_link


class GeoDataService:

    def __init__(self, address):
        self.address = address

    def get_data(self) -> dict:
        """ Return geolocation data (dict) bassed on a passed address.
            If the address does not exist in the external API, return None. """

        data = self._get_data()

        # check if the address exists
        if not data.get('region_name') and not data.get('latitude'):
            return None

        # unpack nested dict
        for key in data['location'].keys():
            data[key] = data['location'][key]
        data.pop('location')

        return data

    def _get_data(self):
        """ Send a GET request on a external geo-data API."""
        try:
            return requests.get(
                geo_api_link(address=self.address)
            ).json()
        except Exception as e:
            print('Error with external API: ', e)
            return dict()