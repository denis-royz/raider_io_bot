from urllib.request import Request, urlopen
from urllib.parse import urlencode


class RaiderIoService:
    headers = {
        "User-Agent": "Fiddler",
        "Host": "raider.io"
    }

    def __init__(self):
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
