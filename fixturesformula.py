import pandas as pd
import json
import os
from sorted_players_data import goalkeepers_sorted, defenders_sorted, midfielders_sorted, forwards_sorted

# Define the paths
players_data_path = "sorted_players_data.py"
fixtures_data_path = "fixtures.csv"
output_file_path = "final_player_data.py"

# Check if the players data file exists
if not os.path.isfile(players_data_path):
    raise FileNotFoundError(f"The file {players_data_path} does not exist. Please check the file path.")

# Load player data with explicit encoding
with open(players_data_path, 'r', encoding='utf-8') as f:
    exec(f.read())

# Check if the fixtures data file exists
if not os.path.isfile(fixtures_data_path):
    raise FileNotFoundError(f"The file {fixtures_data_path} does not exist. Please check the file path.")

# Load fixtures data
fixtures_data = pd.read_csv(fixtures_data_path)

# Ensure correct Gameweek formatting
fixtures_data["Gameweek"] = fixtures_data["Gameweek"].str.replace("GW", "").astype(int)

# Define team abbreviations and coefficients
team_mappings = {
    1: 'ARS', 2: 'AVL', 3: 'BOU', 4: 'BRE', 5: 'BHA', 6: 'CHE', 7: 'CRY', 
    8: 'EVE', 9: 'FUL', 10: 'IPS', 11: 'LEI', 12: 'LIV', 13: 'MCI', 14: 'MUN', 
    15: 'NEW', 16: 'NFO', 17: 'SOU', 18: 'TOT', 19: 'WHU', 20: 'WOL'
}

team_names_to_abbr = {
    'Arsenal': 'ARS', 'Aston Villa': 'AVL', 'Bournemouth': 'BOU', 'Brentford': 'BRE',
    'Brighton': 'BHA', 'Chelsea': 'CHE', 'Crystal Palace': 'CRY', 'Everton': 'EVE',
    'Fulham': 'FUL', 'Ipswich': 'IPS', 'Leicester': 'LEI', 'Liverpool': 'LIV',
    'Man City': 'MCI', 'Man Utd': 'MUN', 'Newcastle': 'NEW', 'Nott\'m Forest': 'NFO',
    'Southampton': 'SOU', 'Spurs': 'TOT', 'West Ham': 'WHU', 'Wolves': 'WOL'
}

""" team_coefficient = {
    'ARS': 0.65, 'AVL': 0.96, 'BOU': 0.99, 'BRE': 1.00, 'BHA': 0.98, 'CHE': 0.83,
    'CRY': 1.05, 'EVE': 1.00, 'FUL': 1.18, 'IPS': 1.48, 'LEI': 1.48, 'LIV': 0.69,
    'MCI': 0.64, 'MUN': 1.20, 'NEW': 0.81, 'NFO': 1.06, 'SOU': 1.48, 'TOT': 0.93,
    'WHU': 1.29, 'WOL': 1.34
} """

team_coefficient = {
    'ARS': 0.825, 'AVL': 0.980, 'BOU': 0.995, 'BRE': 1.000, 'BHA': 0.990, 'CHE': 0.915,
    'CRY': 1.025, 'EVE': 1.000, 'FUL': 1.090, 'IPS': 1.240, 'LEI': 1.240, 'LIV': 0.845,
    'MCI': 0.820, 'MUN': 1.100, 'NEW': 0.905, 'NFO': 1.030, 'SOU': 1.240, 'TOT': 0.965,
    'WHU': 1.145, 'WOL': 1.170
}

home_coefficient = 1.0685
away_coefficient = 0.9315

def adjust_points(player, opponent_team, is_home):
    raw_points = player["xP"]
    team_abbr = team_mappings.get(player["team"], 'UNKNOWN')
    team_coef = team_coefficient.get(opponent_team, 1)  # Default to 1 if not found

    # Initialize adjusted points
    home_adj_points = 0
    away_adj_points = 0

    if is_home:
        home_adj_points = raw_points * home_coefficient
        adjusted_points = home_adj_points * team_coef
    else:
        away_adj_points = raw_points * away_coefficient
        adjusted_points = away_adj_points * team_coef

    return round(adjusted_points, 2)

def calculate_adjusted_points(player_data, fixtures_data, start_gw, end_gw):
    adjusted_points_dict = {}

    for player in player_data:
        player_id = player["id"]
        adjusted_points_dict[player_id] = {f"GW{gw}": 0 for gw in range(start_gw, end_gw + 1)}

    for gw in range(start_gw, end_gw + 1):
        gw_fixtures = fixtures_data[fixtures_data["Gameweek"] == gw]

        for _, fixture in gw_fixtures.iterrows():
            home_team_full = fixture["Home Team"]
            away_team_full = fixture["Away Team"]

            home_team = team_names_to_abbr.get(home_team_full, 'UNKNOWN')
            away_team = team_names_to_abbr.get(away_team_full, 'UNKNOWN')

            for player in player_data:
                team_id = player["team"]
                team_abbr = team_mappings.get(team_id, 'UNKNOWN')

                if team_abbr == home_team:
                    opponent_team = away_team
                    is_home = True
                elif team_abbr == away_team:
                    opponent_team = home_team
                    is_home = False
                else:
                    continue

                adj_points = adjust_points(player, opponent_team, is_home)
                adjusted_points_dict[player["id"]][f"GW{gw}"] = adj_points

    return adjusted_points_dict

# Format player data function
def format_player_data(player_data):
    formatted_data = []
    all_players = goalkeepers_sorted + defenders_sorted + midfielders_sorted + forwards_sorted
    for player_id, gw_points in player_data.items():
        player = next((p for p in all_players if p["id"] == player_id), {})
        formatted_data.append({
            "id": player_id,
            "name": player.get("name", "UNKNOWN"),
            "position": player.get("position", "UNKNOWN"),
            "team": team_mappings.get(player.get("team"), 'UNKNOWN'),
            "price": player.get("cost", "UNKNOWN"),
            **{f"{gw}": f"{points:.2f}" for gw, points in gw_points.items()}
        })
    return formatted_data

# Calculate adjusted points for goalkeepers, defenders, midfielders, and forwards
goalkeepers_points = calculate_adjusted_points(goalkeepers_sorted, fixtures_data, 1, 8)
defenders_points = calculate_adjusted_points(defenders_sorted, fixtures_data, 1, 8)
midfielders_points = calculate_adjusted_points(midfielders_sorted, fixtures_data, 1, 8)
forwards_points = calculate_adjusted_points(forwards_sorted, fixtures_data, 1, 8)

# Combine all player data
combined_player_data = {**goalkeepers_points, **defenders_points, **midfielders_points, **forwards_points}

# Format the combined player data
formatted_combined_player_data = format_player_data(combined_player_data)

# Write data to final_player_data.py with each player on a separate line
output_file_path = 'final_player_data.py'
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write("player_gameweek_data = [\n")
    for player in formatted_combined_player_data:
        f.write(f"    {json.dumps(player, ensure_ascii=False)},\n")
    f.write("]\n")
