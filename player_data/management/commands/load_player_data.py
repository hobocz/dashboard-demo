from django.core.management.base import BaseCommand, CommandError
import json
import pandas as pd
import numpy as np
from django.db import transaction
from player_data.models import Player, Batting, Pitching


class Command(BaseCommand):
    help = 'Performs a simple ETL process for player data'

    def add_arguments(self, parser):
        parser.add_argument("data_file", type=str)

    def handle(self, *args, **options):
        # ========== Read and parse the data into 3 pandas DataFrames ==========
        # ========== Each DataFrame correlates to a Model ==========
        self.stdout.write('Importing file...')
        with open('players.json', 'r') as f:
            file_data = json.load(f)

        self.stdout.write('Parsing data...')
        player_data = []
        batting_data = []
        pitching_data = []
        for player in file_data:
            player_id = player.get('id')
            stats = player.pop('stats')
            player_data.append(player)
            if stats:
                for batting in stats.get('batting', []):
                    batting['player'] = player_id
                    batting_data.append(batting)
                for pitching in stats.get('pitching', []):
                    pitching['player'] = player_id
                    pitching_data.append(pitching)
        players_df = pd.DataFrame(player_data)
        batting_df = pd.DataFrame(batting_data)
        pitching_df = pd.DataFrame(pitching_data)

        # ========== Perform any validation and/or transformation ==========
        self.stdout.write('Validation & transformation...')
        players_issues = players_df[(players_df['id'].isna()) | (~players_df['id'].apply(lambda x: isinstance(x, (int, float))))]
        if len(players_issues) > 0:
            self.stdout.write('The following players have an invalid "id" value:')
            print(players_issues[['id','name_first', 'name_last']])
            #return
        players_issues = players_df[(players_df['name_last'].isna()) | (players_df['name_last'].str.len() == 0)]
        if len(players_issues) > 0:
            self.stdout.write('The following players do not have a "name_last" value:')
            print(players_issues[['id','name_first', 'name_last']])
            #return
        players_issues = players_df[players_df['height_inches'].isna()]
        if len(players_issues) > 0:
            self.stdout.write('The following players do not have a "height_inches" value:')
            self.stdout.write('--- Substitute will be 0')
            print(players_issues[['id','name_first', 'name_last', 'height_inches']])
            players_df['height_inches'] = players_df['height_inches'].fillna(0)
            
        team_list = ['BAL', 'BOS', 'NYY', 'TB', 'TOR', 'CWS', 'CLE', 'DET', 'KC', 'MIN', 'HOU', 'LAA', 'OAK', 'SEA', 'TEX', 'ATL', 'MIA', 'NYM', 'PHI', 'WSH', 'CHC', 'CIN', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SD', 'SF']
        players_issues = players_df[~players_df['team'].isin(team_list)]
        if len(players_issues) > 0:
            self.stdout.write('The following players don\'t have a recognized "team" value:')
            print(players_issues[['id','name_first', 'name_last', 'team']])
            #return

        players_df = players_df.replace(np.nan, None)
        batting_df = batting_df.replace(np.nan, None)
        pitching_df = pitching_df.replace(np.nan, None)

        # ========== Create Model objects from the DataFrames and load ==========
        self.stdout.write('Loading data...')
        with transaction.atomic():  # Ensures all inserts happen or none
            player_update_fields = [field.name for field in Player._meta.get_fields() if field.concrete and field.name != "id"]
            player_list = []
            for _, row in players_df.iterrows():
                row_dict = row.to_dict()
                player_list.append(Player(**row_dict))
            player_result = Player.objects.bulk_create(player_list, update_conflicts=True, update_fields=player_update_fields, unique_fields=['id'])
            self.stdout.write(f'Player create/update count: {len(player_result)}')

            batting_update_fields = [field.name for field in Batting._meta.get_fields() if field.concrete and field.name != "id"]
            batting_list = []
            for _, row in batting_df.iterrows():
                row_dict = row.to_dict()
                row_dict['player'] = Player.objects.get(id=row_dict['player'])
                batting_list.append(Batting(**row_dict))
            batting_result = Batting.objects.bulk_create(batting_list, update_conflicts=True, update_fields=batting_update_fields, unique_fields=['id'])
            self.stdout.write(f'Batting stats create/update count: {len(batting_result)}')

            pitching_update_fields = [field.name for field in Pitching._meta.get_fields() if field.concrete and field.name != "id"]
            pitching_list = []
            for _, row in pitching_df.iterrows():
                row_dict = row.to_dict()
                row_dict['player'] = Player.objects.get(id=row_dict['player'])
                pitching_list.append(Pitching(**row_dict))
            pitching_result = Pitching.objects.bulk_create(pitching_list, update_conflicts=True, update_fields=pitching_update_fields, unique_fields=['id'])
            self.stdout.write(f'Pitching stats create/update count: {len(pitching_result)}')