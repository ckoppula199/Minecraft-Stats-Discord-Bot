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
        with open('UUIDs.json', 'r+') as UUID_file:
            file_data = json.load(UUID_file)
            file_data.update({username: uuid})
            UUID_file.seek(0)
            UUID_file.truncate()
            json.dump(file_data, UUID_file)
        return uuid

    def get_bedwars_data(self, username, prefix):
        uuid = self.get_uuid(username)
        bedwars_data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'uuid':uuid})["player"]["stats"]["Bedwars"]
        game_data = {}

        stats = ['Kills', 'Deaths', 'Final Kills', 'Final Deaths', 'Beds Broken', 'Beds Lost', 'Wins', 'Losses', 'Iron Collected', 'Gold Collected', 'Diamonds Collected', 
                'Emeralds Collected', 'Games Played']

        suffixes = ['_kills_bedwars', '_deaths_bedwars', '_final_kills_bedwars', '_final_deaths_bedwars', '_beds_broken_bedwars', '_beds_lost_bedwars', '_wins_bedwars',
                    '_losses_bedwars', '_iron_resources_collected_bedwars', '_gold_resources_collected_bedwars', '_diamond_resources_collected_bedwars',
                    '_emerald_resources_collected_bedwars', '_games_played_bedwars']

        for stat, suffix in zip(stats, suffixes):
            try:
                game_data[stat] = bedwars_data[prefix + suffix]
            except KeyError:
                game_data[stat] = 0

        return game_data

    def bedwars_stats_text(self, game_data):
        msg = ''
        for key, value in game_data.items():
            line = f'{key}: {value}\n'
            msg += line

        wins = game_data.get('Wins', None)
        losses = game_data.get('Losses', None)
        if wins is not None and losses is not None and losses != 0 and wins != 0:
            win_percent = (wins / (wins + losses))* 100
            msg += f'Win Percentage: {win_percent:.2f}%\n'

        kills = game_data.get('Kills', None)
        deaths = game_data.get('Deaths', None)
        if kills is not None and deaths is not None and deaths != 0:
            kd_ratio = kills / deaths
            msg += f'K/D Ratio: {kd_ratio:.2f}\n'
        return msg


    def bedwars_stats_solos(self, username):
        game_data = self.get_bedwars_data(username, 'eight_one')
        msg = self.bedwars_stats_text(game_data)
        return msg

    def bedwars_stats_duos(self, username):
        game_data = self.get_bedwars_data(username, 'eight_two')
        msg = self.bedwars_stats_text(game_data)
        return msg

    def bedwars_stats_trios(self, username):        
        game_data = self.get_bedwars_data(username, 'four_three')
        msg = self.bedwars_stats_text(game_data)
        return msg

    def bedwars_stats_quads(self, username):
        game_data = self.get_bedwars_data(username, 'four_four')
        msg = self.bedwars_stats_text(game_data)
        return msg

    def bedwars_stats_practice(self, username):
        uuid = self.get_uuid(username)
        bedwars_data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'uuid':uuid})["player"]["stats"]["Bedwars"]["practice"]
        msg = json.dumps(bedwars_data, indent=4)
        return msg

    def zombies_stats(self):
        pass

    def build_battle_stats(self, username):
        uuid = self.get_uuid(username)
        build_battle_data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'uuid':uuid})["player"]["stats"]["BuildBattle"]
        stats = ['Solo Wins', 'Team Wins', 'Guess the Build Wins', 'Correct Guesses', 'Total Votes Cast', 'Games Played']
        keys = ['wins_solo_normal', 'wins_teams_normal', 'wins_guess_the_build', 'correct_guesses', 'total_votes', 'games_played']
        msg = ''
        for stat, key in zip(stats, keys):
            try:
                line = f'{stat}: {build_battle_data[key]}\n'
                msg += line
            except KeyError:
                line = f'{stat}: 0\n'
                msg += line
        return msg

# Used for debugging the above class
if __name__ == "__main__":
    hypixel_stats = HypixelStats()
    print(hypixel_stats.HYPIXEL_API_KEY)