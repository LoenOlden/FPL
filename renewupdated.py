from updated_player_data import players_data
"""
team_mappings = {
    1: 'ARS', 2: 'AVL', 3: 'BOU', 4: 'BRE', 5: 'BHA', 6: 'CHE', 7: 'CRY', 
    8: 'EVE', 9: 'FUL', 10: 'IPS', 11: 'LEI', 12: 'LIV', 13: 'MCI', 14: 'MUN', 
    15: 'NEW', 16: 'NFO', 17: 'SOU', 18: 'TOT', 19: 'WHU', 20: 'WOL'
}

team_offense = {
    "MCI": 2.133, "LIV": 2.058, "TOT": 1.955, "CHE": 1.818, "ARS": 1.78, 
    "BOU": 1.685, "AVL": 1.638, "FUL": 1.585, "NEW": 1.563, "MUN": 1.553, 
    "BRE": 1.548, "BHA": 1.533, "WHU": 1.393, "CRY": 1.37, "NFO": 1.365, 
    "EVE": 1.293, "SOU": 1.17, "WOL": 1.168, "IPS": 1.11, "LEI": 1.11
}

team_defense = {
    "LIV": 1.08, "ARS": 1.09, "MCI": 1.205, "NFO": 1.305, "FUL": 1.315, 
    "TOT": 1.355, "AVL": 1.388, "CHE": 1.433, "BOU": 1.473, "NEW": 1.50, 
    "EVE": 1.515, "BHA": 1.55, "MUN": 1.608, "CRY": 1.61, "BRE": 1.74, 
    "WHU": 1.778, "WOL": 1.78, "LEI": 2.02, "IPS": 2.05, "SOU": 2.10
}

average_save = {
    'LIV': 2.71,
    'ARS': 2.48,
    'MCI': 2.19,
    'NFO': 2.71,
    'FUL': 3.00,
    'TOT': 2.47,
    'AVL': 2.57,
    'CHE': 3.32,
    'BOU': 3.78,
    'NEW': 3.75,
    'EVE': 2.71,
    'BHA': 3.19,
    'MUN': 2.96,
    'CRY': 3.14,
    'BRE': 4.53,
    'WHU': 3.24,
    'WOL': 3.41,
    'LEI': 3.83,
    'IPS': 3.83,
    'SOU': 4.25
}

team_data = {
    team_id: {
        "TeamXG90": team_offense.get(team_name, 0),
        "TeamXGC90": team_defense.get(team_name, 0)
    }
    for team_id, team_name in team_mappings.items()
}

# Build a team data dictionary with save coefficients
team_save_data = {
    team_name: average_save.get(team_name, 0) 
    for team_name in team_mappings.values()
}

# Update player data
for player in players_data:
    team_name = team_mappings.get(player["team"])  # Get the team name using team_id
    if team_name:
        team_id = player["team"]
        player["saves"] = team_save_data.get(team_name, 0)
        player["TeamXG90"] = team_data[team_id]["TeamXG90"]
        player["TeamXGC90"] = team_data[team_id]["TeamXGC90"]

# Write back to the file
with open("updated_player_data.py", "w", encoding='utf-8') as file:
    file.write("players_data = [\n")
    for player in players_data:
        file.write(f"    {player},\n")
    file.write("]\n")
"""

team_mappings = {
    1: 'ARS', 2: 'AVL', 3: 'BOU', 4: 'BRE', 5: 'BHA', 6: 'CHE', 7: 'CRY', 
    8: 'EVE', 9: 'FUL', 10: 'IPS', 11: 'LEI', 12: 'LIV', 13: 'MCI', 14: 'MUN', 
    15: 'NEW', 16: 'NFO', 17: 'SOU', 18: 'TOT', 19: 'WHU', 20: 'WOL'
}

team_coef_Def = {
    'LIV': 0.699, 'ARS': 0.706, 'MCI': 0.780, 'NFO': 0.845, 'FUL': 0.851,
    'TOT': 0.877, 'AVL': 0.898, 'CHE': 0.928, 'BOU': 0.953, 'NEW': 0.971,
    'EVE': 0.981, 'BHA': 1.003, 'MUN': 1.041, 'CRY': 1.042, 'BRE': 1.126,
    'WHU': 1.151, 'WOL': 1.152, 'LEI': 1.307, 'IPS': 1.327, 'SOU': 1.359
}

team_coef_Att = {
    'MCI': 0.722, 'LIV': 0.749, 'TOT': 0.788, 'CHE': 0.848, 'ARS': 0.866,
    'BOU': 0.915, 'AVL': 0.941, 'FUL': 0.972, 'NEW': 0.986, 'MUN': 0.992,
    'BRE': 0.995, 'BHA': 1.005, 'WHU': 1.106, 'CRY': 1.125, 'NFO': 1.129,
    'EVE': 1.192, 'SOU': 1.317, 'WOL': 1.319, 'IPS': 1.388, 'LEI': 1.388
}

team_data = {
    team_id: {
        "TeamDefCoef": team_coef_Def.get(team_name, 0),
        "TeamAttCoef": team_coef_Att.get(team_name, 0)
    }
    for team_id, team_name in team_mappings.items()
}

# Update player data
for player in players_data:
    team_name = team_mappings.get(player["team"])
    if team_name:
        team_id = player["team"]
        player["TeamDefCoef"] = team_data[team_id]["TeamDefCoef"]
        player["TeamAttCoef"] = team_data[team_id]["TeamAttCoef"]

# Write back to the file
with open("updated_player_data.py", "w", encoding='utf-8') as file:
    file.write("players_data = [\n")
    for player in players_data:
        file.write(f"    {player},\n")
    file.write("]\n")