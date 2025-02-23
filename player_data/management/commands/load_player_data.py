from django.core.management.base import BaseCommand
import json
import pandas as pd
import numpy as np
from django.db import transaction
from player_data.models import Player, Batting, Pitching


class Command(BaseCommand):
    """ Performs a simple ETL process for the purposes of this demo project

    1. Extract = simply uses json.load() & then parses the data into pandas DataFrames
    2. Transform = Things like Spark, dbt, Airflow etc, all seemed totally
        out of scope. So pandas is used for validation and transformation... and to
        demonstrate proficiency with pandas!
        (it's always useful to have pandas in your back pocket :)
    3. Load = uses Django ORM
    """
    help = 'Performs a simple ETL process for player data'

    def add_arguments(self, parser):
        parser.add_argument('data_file', type=str)

    def handle(self, *args, **options):
        # ========== EXTRACT ==========
        # Read and parse the data into 3 pandas DataFrames
        # Each DataFrame correlates to a Model
        self.stdout.write('Importing file...')
        with open(options['data_file'], 'r') as f:
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

        # ========== TRANSFORM ==========
        # Perform any validation and/or transformation
        # NOTE: This is just a very small sample of possibilities. In 
        # production these would be fully fleshed out and likely 
        # separated into their own module.
        self.stdout.write('Validation & transformation...')
        # Check for player IDs: not null and numeric
        players_issues = players_df[(players_df['id'].isna()) | 
                                    (~players_df['id'].apply(lambda x: isinstance(x,(int,float))))]
        if len(players_issues) > 0:
            self.stdout.write('++++++++++++++++++++')
            self.stdout.write('The following players have an invalid "id" value:')
            print(players_issues[['id','name_first', 'name_last']])
            self.stdout.write('!!! Process cancelled !!!')
            return
        # Check player last name: not null and not empty string
        players_issues = players_df[(players_df['name_last'].isna()) | 
                                    (players_df['name_last'].str.len() == 0)]
        if len(players_issues) > 0:
            self.stdout.write('++++++++++++++++++++')
            self.stdout.write('The following players do not have a "name_last" value:')
            print(players_issues[['id','name_first', 'name_last']])
            self.stdout.write('--- Substituting "unknown" and continuing...')
            players_df['name_last'] = players_df['name_last'].fillna('unknown')
            players_df['name_last'] = players_df['name_last'].replace('', 'unknown')
            # return?
        # Check player height: not null
        players_issues = players_df[players_df['height_inches'].isna()]
        if len(players_issues) > 0:
            self.stdout.write('++++++++++++++++++++')
            self.stdout.write('The following players do not have a "height_inches" value:')
            print(players_issues[['id','name_first', 'name_last', 'height_inches']])
            self.stdout.write('--- No transform and continuing...')
            # OR...
            # self.stdout.write('--- Substituting 0 and continuing...')
            # players_df['height_inches'] = players_df['height_inches'].fillna(0)
            # return?
        # Check player team: is valid from list
        team_list = ['BAL', 'BOS', 'NYY', 'TB', 'TOR', 'CWS', 'CLE', 'DET',
                     'KC', 'MIN', 'HOU', 'LAA', 'OAK', 'SEA', 'TEX', 'ATL', 
                     'MIA', 'NYM', 'PHI', 'WSH', 'CHC', 'CIN', 'MIL', 'PIT',
                     'STL', 'ARI', 'COL', 'LAD', 'SD', 'SF']
        players_issues = players_df[~players_df['team'].isin(team_list)]
        if len(players_issues) > 0:
            self.stdout.write('++++++++++++++++++++')
            self.stdout.write('The following players don\'t have a recognized "team" value:')
            print(players_issues[['id','name_first', 'name_last', 'team']])
            self.stdout.write('--- No transform and continuing...')
            # return?

        # After the above transformations, replace all NaN with None
        # (loading process doesn't understand NaN)
        players_df = players_df.replace(np.nan, None)
        batting_df = batting_df.replace(np.nan, None)
        pitching_df = pitching_df.replace(np.nan, None)

        # ========== LOAD ==========
        # Create Model objects from the DataFrames and load
        self.stdout.write('Loading data...')
        with transaction.atomic():
            # Since Player objects come with a unique id, we can use 
            # bulk_create() to do a 'create or update' process, preserving
            # the orignal database assigned ids (if we ever need them)
            player_update_fields = [field.name for field in Player._meta.get_fields() if field.concrete and field.name != "id"]
            player_list = []
            for _, row in players_df.iterrows():
                row_dict = row.to_dict()
                player_list.append(Player(**row_dict))
            player_result = Player.objects.bulk_create(player_list, update_conflicts=True, update_fields=player_update_fields, unique_fields=['id'])
            self.stdout.write(f'Player create/update count: {len(player_result)}')

            # However Batting and Pitching objects don't come with unique ids,
            # so we just flush the tables and reload
            Batting.objects.all().delete()
            batting_list = []
            for _, row in batting_df.iterrows():
                row_dict = row.to_dict()
                row_dict['player'] = Player.objects.get(id=row_dict['player'])
                batting_list.append(Batting(**row_dict))
            batting_result = Batting.objects.bulk_create(batting_list)
            self.stdout.write(f'Batting stats recreate count: {len(batting_result)}')

            Pitching.objects.all().delete()
            pitching_list = []
            for _, row in pitching_df.iterrows():
                row_dict = row.to_dict()
                row_dict['player'] = Player.objects.get(id=row_dict['player'])
                pitching_list.append(Pitching(**row_dict))
            pitching_result = Pitching.objects.bulk_create(pitching_list)
            self.stdout.write(f'Pitching stats recreate count: {len(pitching_result)}')