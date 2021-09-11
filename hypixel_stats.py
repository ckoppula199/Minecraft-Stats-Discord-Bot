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

    def constuct_stats_message(self, stats, keys, data):
        msg = ''
        for stat, key in zip(stats, keys):
            try:
                line = f'{stat}: {data[key]}\n'
                msg += line
            except KeyError:
                line = f'{stat}: 0\n'
                msg += line
        return msg

    def zombies_kills_stats(self, username):
        uuid = self.get_uuid(username)
        zombies_data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'uuid':uuid})["player"]["stats"]["Arcade"]
        stats = ['Basic Zombie Kills', 'Blaze Zombie Kills', 'Fire Zombie Kills', 'Magma Zombie Kills', 'Magma Cube Zombie Kills', 'Pig Zombie Kills', 'TNT Zombie Kills', 'TNT Baby Zombie Kills',
                 'Wolf Zombie Kills', 'Guardian Zombie Kills', 'Empowered Zombie Kills', 'Silverfish Zombie Kills', 'Skeleton Zombie Kills', 'Ender Zombie Kills', 'Endermite Zombie Kills']
        keys = ['basic_zombie_kills_zombies', 'blaze_zombie_kills_zombies', 'fire_zombie_kills_zombies', 'magma_zombie_kills_zombies', 'magma_cube_zombie_kills_zombies', 'pig_zombie_zombie_kills_zombies',
                'tnt_zombie_kills_zombies', 'tnt_baby_zombie_kills_zombies', 'wolf_zombie_kills_zombies', 'guardian_zombie_kills_zombies', 'empowered_zombie_kills_zombies', 'silverfish_zombie_kills_zombies',
                'skelefish_zombie_kills_zombies', 'ender_zombie_kills_zombies', 'endermite_zombie_kills_zombies']
        msg = self.constuct_stats_message(stats, keys, zombies_data)
        return msg

    def zombies_general_stats(self, username):
        uuid = self.get_uuid(username)
        zombies_data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'uuid':uuid})["player"]["stats"]["Arcade"]
        stats = ['Best Round', 'Bullets Shot', 'Bullets Hit', 'Doors Opened', 'Windows Repaired', 'Headshots', 'Deaths', 'Times Knocked Down', 'Total Rounds Survived',
                 'Total Kills', 'Player Revives', 'Fastest time to round 10', 'Fastest time to round 20']
        keys = ['best_round_zombies', 'bullets_shot_zombies', 'bullets_hit_zombies', 'doors_opened_zombies', 'windows_repaired_zombies', 'headshots_zombies', 'deaths_zombies',
                'times_knocked_down_zombies', 'total_rounds_survived_zombies', 'zombie_kills_zombies', 'players_revived_zombies', 'fastest_time_10_zombies', 'fastest_time_20_zombies']
        msg = self.constuct_stats_message(stats, keys, zombies_data)
        shots = zombies_data.get('bullets_shot_zombies', None)
        hits = zombies_data.get('bullets_hit_zombies', None)
        if shots is not None and hits is not None and hits != 0 and shots != 0:
            accuracy = (hits / (hits + shots)) * 100
            msg += f'Shot Accuracy: {accuracy:.2f}%\n'
        return msg

    def build_battle_stats(self, username):
        uuid = self.get_uuid(username)
        build_battle_data = self.query_hypixel_api({'key': self.HYPIXEL_API_KEY, 'uuid':uuid})["player"]["stats"]["BuildBattle"]
        stats = ['Solo Wins', 'Team Wins', 'Guess the Build Wins', 'Correct Guesses', 'Total Votes Cast', 'Games Played']
        keys = ['wins_solo_normal', 'wins_teams_normal', 'wins_guess_the_build', 'correct_guesses', 'total_votes', 'games_played']
        msg = self.constuct_stats_message(stats, keys, build_battle_data)
        return msg

# Used for debugging the above class
if __name__ == "__main__":
    hypixel_stats = HypixelStats()
    print(hypixel_stats.HYPIXEL_API_KEY)