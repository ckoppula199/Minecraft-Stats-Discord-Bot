import requests
import json

class HypixelStats:

    def __init__(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        self.HYPIXEL_API_KEY = config['key']

    def query_hypixel_api(self, params):
        data = requests.get(
            url = "https://api.hypixel.net/player",
            params = params
        ).json()

        return data

    def get_uuid(self, username):
        with open('UUIDs.json', 'r') as UUID_file:
            uuids = json.load(UUID_file)

        username_uuid = uuids.get(username, None)

        if username_uuid is not None:
            return username_uuid

        return self.store_uuid(username)

    def store_uuid(self, username):
        data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'name':username})
        uuid = data['player']['uuid']
        with open('UUIDs.json', 'w') as UUID_file:
            json.dump({username: uuid}, UUID_file)
        return uuid
    
if __name__ == "__main__":
    hypixel_stats = HypixelStats()
    print(hypixel_stats.HYPIXEL_API_KEY)

