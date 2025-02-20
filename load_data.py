import json
import pandas as pd
from django.db import transaction
from player_data.models import Player, Batting, Pitching


# Step 1: Read JSON file
with open('players.json', 'r') as f:
    file_data = json.load(f)

# Step 2: Extract player data
player_data = []
batting_data = []
pitching_data = []
for player in file_data:
    player_id = player.get('id')
    player_data.append({
        'id': player_id,
        'name_first': player.get('name_first'), 
        'name_use': player.get('name_use')
    })
    for batting in player.get('stats', {}).get('batting'):
        batting_data.append({
            'player': player_id,
            'year': batting.get('year'),
            'runs': batting.get('runs'),
        })
    for pitching in player.get('stats', {}).get('pitching'):
        pitching_data.append({
            'player': player_id,
            'year': pitching.get('year'),
            'wins': pitching.get('wins'),
        })
players_df = pd.DataFrame(player_data)
batting_df = pd.DataFrame(batting_data)
pitching_df = pd.DataFrame(pitching_data)

# Step 4: Validate Data
# try:
#     validated_players = PlayerSchema.validate(players_df)
#     validated_pitching = PitchingSchema.validate(pitching_df)
#     print("✅ Data validation successful!")
# except pa.errors.SchemaError as e:
#     print("❌ Data validation failed!", e)
#     return

# Step 5: Load into Django DB
with transaction.atomic():  # Ensures all inserts happen or none
    players = [
        Player(id=row["id"], name_first=row["name_first"], name_use=row["name_use"])
        for _, row in validated_players.iterrows()
    ]
    Player.objects.bulk_create(players, ignore_conflicts=True)

    pitching_stats = [
        PitchingStat(player_id=row["player_id"], year=row["year"], league=row["league"])
        for _, row in validated_pitching.iterrows()
    ]
    PitchingStat.objects.bulk_create(pitching_stats, ignore_conflicts=True)

print("✅ Data successfully loaded into the database!")
