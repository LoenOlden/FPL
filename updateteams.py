import pandas as pd

# Define the path to the CSV file
csv_file = "players_data.csv"
df = pd.read_csv(csv_file)

# Extract and rename relevant columns
df = df[['id', 'web_name', 'team', 'position', 'cost', 'minutes', 'saves_per_90', 'starts', 'expected_goals_per_90', 'expected_assists_per_90', 'expected_goals_conceded_per_90']]
df.rename(columns={
    'expected_goals_per_90': 'xG90',
    'expected_assists_per_90': 'xA90',
    'expected_goals_conceded_per_90': 'xGC90'
}, inplace=True)

# Team mappings
team_mappings = {
    1: ('ARS', 'Arsenal'),
    2: ('AVL', 'Aston Villa'),
    3: ('BOU', 'Bournemouth'),
    4: ('BRE', 'Brentford'),
    5: ('BHA', 'Brighton'),
    6: ('CHE', 'Chelsea'),
    7: ('CRY', 'Crystal Palace'),
    8: ('EVE', 'Everton'),
    9: ('FUL', 'Fulham'),
    10: ('IPS', 'Ipswich'),
    11: ('LEI', 'Leicester'),
    12: ('LIV', 'Liverpool'),
    13: ('MCI', 'Man City'),
    14: ('MUN', 'Man Utd'),
    15: ('NEW', 'Newcastle'),
    16: ('NFO', 'Nott\'m Forest'),
    17: ('SOU', 'Southampton'),
    18: ('TOT', 'Spurs'),
    19: ('WHU', 'West Ham'),
    20: ('WOL', 'Wolves')
}

# New team statistics
team_stats = {
    'ARS': (0.436, 0.192, 0.01, 0.168, 0.003),
    'AVL': (0.210, 0.389, 0.068, 0.496, 0.083),
    'BOU': (0.202, 0.396, 0.073, 0.527, 0.115),
    'BRE': (0.2102, 0.389, 0.068, 0.508, 0.093),
    'BHA': (0.232, 0.368, 0.057, 0.460, 0.060),
    'CHE': (0.2101, 0.389, 0.068, 0.523, 0.109),
    'CRY': (0.239, 0.361, 0.054, 0.429, 0.046),
    'EVE': (0.223, 0.377, 0.061, 0.502, 0.088),
    'FUL': (0.190, 0.407, 0.080, 0.537, 0.133),
    'IPS': (0.147, 0.443, 0.115, 0.532, 0.250),
    'LEI': (0.147, 0.443, 0.115, 0.532, 0.250),
    'LIV': (0.292, 0.312, 0.035, 0.472, 0.066),
    'MCI': (0.387, 0.230, 0.016, 0.307, 0.016),
    'MUN': (0.159, 0.434, 0.104, 0.547, 0.174),
    'NEW': (0.204, 0.394, 0.072, 0.537, 0.133),
    'NFO': (0.230, 0.370, 0.058, 0.429, 0.046),
    'SOU': (0.147, 0.443, 0.115, 0.532, 0.250),
    'TOT': (0.200, 0.398, 0.074, 0.475, 0.068),
    'WHU': (0.147, 0.443, 0.115, 0.532, 0.250),
    'WOL': (0.164, 0.430, 0.100, 0.543, 0.151)
}

# Add new statistics to players based on team
for team_id, (abbr, _) in team_mappings.items():
    csP, xgc23, xgc45, shots3, shots6 = team_stats[abbr]
    df.loc[df['team'] == team_id, ['csP', 'xgc23', 'xgc45', '3shots', '6shots']] = csP, xgc23, xgc45, shots3, shots6

# Convert DataFrame to dictionary format required for the Python script
teams_data = {}
for team_id in df['team'].unique():
    team_players = df[df['team'] == team_id].to_dict('records')
    teams_data[team_id] = team_players

# Format data for Python script
with open("updated_teams_data.py", "w", encoding="utf-8") as f:
    f.write("teams_data = {\n")
    for team_id, players in teams_data.items():
        f.write(f"    {team_id}: [\n")
        for player in players:
            f.write("        {")
            player_data = ", ".join([f'"{k}": {repr(v)}' for k, v in player.items()])
            f.write(player_data)
            f.write("},\n")
        f.write("    ],\n")
    f.write("}\n")

print("Updated team data saved to 'updated_teams_data.py'")