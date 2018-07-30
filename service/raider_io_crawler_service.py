from urllib.request import Request, urlopen
import json


class RaiderIoService:

    headers = {
        "User-Agent": "Fiddler",
        "Host": "raider.io",
        "Content-Type": "application/json; charset=utf-8"
    }

    def __init__(self):
        self.base_url = 'https://raider.io/api/'

    def call_character_crawler(self, realm_id, realm, region, character):
        crawler_url = self.base_url + 'crawler/characters'
        body = {
            "realmId": realm_id,
            "realm": realm,
            "region": region,
            "character": character
        }
        params = json.dumps(body).replace(' ', '').encode('utf8')
        print(crawler_url)
        print(params)
        request = Request(crawler_url, data=params, headers=self.headers, method='POST')
        with urlopen(request) as f:
            print(f.read().decode('utf-8'))
        pass

    def call_dungeon_crawler(self, realm_id, realm, region, dungeon):
        crawler_url = self.base_url + 'crawler/dungeons'
        body = {
            "realmId": realm_id,
            "realm": realm,
            "region": region,
            "dungeon": dungeon
        }
        params = json.dumps(body).replace(' ', '').encode('utf8')
        print(crawler_url)
        print(params)
        request = Request(crawler_url, data=params, headers=self.headers, method='POST')
        with urlopen(request) as f:
            print(f.read().decode('utf-8'))
        pass

    def update(self, subscriptions):
        realms = []
        for sub in subscriptions:
            realm = sub['realm']
            region = sub['region']
            character_name = sub['character_name']
            self.call_character_crawler(614, realm, region, character_name)
            if realm not in realms:
                realms.append(realm)
        for realm in realms:
            self.call_dungeon_crawler(614, realm, 'eu', 'black-rook-hold')
        pass
