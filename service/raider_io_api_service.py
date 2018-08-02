from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json


class RaiderIoService:
    headers = {
        "User-Agent": "Fiddler",
        "Host": "raider.io"
    }

    def __init__(self, database_service):
        self.base_url = 'https://raider.io/api/v1/'

    def get_character_profile(self, realm, region, character):
        params = {
            'region': region,
            'realm': realm,
            'name': character
        }
        url_parts = urlencode(params)
        request_url = self.base_url + 'characters/profile?' + url_parts
        request = Request(request_url, headers=self.headers, method='GET')
        with urlopen(request) as f:
            return f.read().decode('utf-8')

    def get_mythic_affixes(self, region='eu', locale='en'):
        """
        :param region: Name of region to look up affixes for. Can be one of: us, eu, kr, tw
        :param locale: Language to return name and description of affixes in.
         Can be one of: en, ru, ko, cn, pt, it, fr, es, de, tw
        :return: see https://raider.io/api#!/mythic95plus/get_api_v1_mythic_plus_affixes
        """
        params = {
            'region': region,
            'locale': locale
        }
        url_parts = urlencode(params)
        request_url = self.base_url + 'mythic-plus/affixes?' + url_parts
        request = Request(request_url, headers=self.headers, method='GET')
        with urlopen(request) as f:
            return json.loads(f.read().decode('utf-8'))

    def update(self, subscriptions):
        realms = []
        results = []
        for sub in subscriptions:
            realm = sub['realm']
            region = sub['region']
            character_name = sub['character_name']
            results.append(self.get_character_profile(realm, region, character_name))
            if realm not in realms:
                realms.append(realm)
        return results
