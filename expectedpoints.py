import numpy as np
import pandas as pd
from scipy.stats import poisson
import json
from updated_player_data import players_data

fixtures_data_path = "fixtures.csv"
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

team_xg90 = {
    "MCI": 2.133, "LIV": 2.058, "TOT": 1.955, "CHE": 1.818, "ARS": 1.78, 
    "BOU": 1.685, "AVL": 1.638, "FUL": 1.585, "NEW": 1.563, "MUN": 1.553, 
    "BRE": 1.548, "BHA": 1.533, "WHU": 1.393, "CRY": 1.37, "NFO": 1.365, 
    "EVE": 1.293, "SOU": 1.17, "WOL": 1.168, "IPS": 1.11, "LEI": 1.11
}

team_xgc90 = {
    "LIV": 1.08, "ARS": 1.09, "MCI": 1.205, "NFO": 1.305, "FUL": 1.315, 
    "TOT": 1.355, "AVL": 1.388, "CHE": 1.433, "BOU": 1.473, "NEW": 1.50, 
    "EVE": 1.515, "BHA": 1.55, "MUN": 1.608, "CRY": 1.61, "BRE": 1.74, 
    "WHU": 1.778, "WOL": 1.78, "LEI": 2.02, "IPS": 2.05, "SOU": 2.10
}

team_names_to_abbr = {
    'Arsenal': 'ARS', 'Aston Villa': 'AVL', 'Bournemouth': 'BOU', 'Brentford': 'BRE',
    'Brighton': 'BHA', 'Chelsea': 'CHE', 'Crystal Palace': 'CRY', 'Everton': 'EVE',
    'Fulham': 'FUL', 'Ipswich': 'IPS', 'Leicester': 'LEI', 'Liverpool': 'LIV',
    'Man City': 'MCI', 'Man Utd': 'MUN', 'Newcastle': 'NEW', 'Nott\'m Forest': 'NFO',
    'Southampton': 'SOU', 'Spurs': 'TOT', 'West Ham': 'WHU', 'Wolves': 'WOL'
}

home_coefficient = 1.147
away_coefficient = 0.853

def poisson_cleansheet(lambda_xgc):
    """Calculates the Poisson distribution for clean sheet probability"""
    prob_0 = poisson.pmf(0, lambda_xgc)
    return prob_0

def poisson_probability_conceding_2_or_3_goals(lambda_xgc):
    prob_2 = poisson.pmf(2, lambda_xgc)
    prob_3 = poisson.pmf(3, lambda_xgc)
    
    prob_2_or_3 = prob_2 + prob_3

    return prob_2_or_3

def poisson_probability_conceding_4_or_5_goals(lambda_xgc):
    prob_4 = poisson.pmf(4, lambda_xgc)
    prob_5 = poisson.pmf(5, lambda_xgc)
    
    prob_4_or_5 = prob_4 + prob_5 

    return prob_4_or_5

def get_opponent_offence_strength(team_name):
    return team_coef_Att.get(team_name, 1)  # Default to 1 if not found

def get_opponent_defense_strength(team_name):
    return team_coef_Def.get(team_name, 1)  # Default to 1 if not found

def calculate_goalkeeper_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        appearance_points = player["expected_minutes"] / 93
        TeamXGC90 = player["TeamXGC90"]
        opponent_xg90 = opponent.get("TeamXG90")
        reversecoeff = 2 - home_away_coefficient
        team_def_coeff = player["TeamDefCoef"]
        opponent_att_coeff = opponent.get("TeamAttCoef")
        lambda_xgc = ((TeamXGC90*1/opponent_att_coeff + opponent_xg90*team_def_coeff) * reversecoeff) / 2
        clean_sheet_probability = poisson_cleansheet(lambda_xgc)
        clean_sheet_points = 4.2 * clean_sheet_probability
        conceding23 = poisson_probability_conceding_2_or_3_goals(lambda_xgc)
        conceding45 = poisson_probability_conceding_4_or_5_goals(lambda_xgc)
        
        offence_strength = get_opponent_offence_strength(opponent["team_name"])
        save_3points = 1.0 * player["3shots"] * 1/offence_strength * reversecoeff
        save_6points = 2.0 * player["6shots"] * 1/offence_strength * reversecoeff
        save_points = save_3points + save_6points
        goal2CPen = -1.0 * conceding23
        goal4CPen = -2.0 * conceding45
        return ((clean_sheet_points + save_points + appearance_points + goal2CPen + goal4CPen + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_defender_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        appearance_points = player["expected_minutes"] / 93
        TeamXGC90 = player["TeamXGC90"]
        opponent_xg90 = opponent.get("TeamXG90")
        reversecoeff = 2 - home_away_coefficient
        team_def_coeff = player["TeamDefCoef"]
        opponent_att_coeff = opponent.get("TeamAttCoef")
        lambda_xgc = ((TeamXGC90*1/opponent_att_coeff + opponent_xg90*team_def_coeff) * reversecoeff) / 2
        clean_sheet_probability = poisson_cleansheet(lambda_xgc)
        clean_sheet_points = 4.2 * clean_sheet_probability

        defense_strength = get_opponent_defense_strength(opponent["team_name"])
        goal_points = player["xG90"] * 6.3 * defense_strength * home_away_coefficient
        assist_points = player["xA90"] * 3.15 * defense_strength * home_away_coefficient

        conceding23 = poisson_probability_conceding_2_or_3_goals(lambda_xgc)
        conceding45 = poisson_probability_conceding_4_or_5_goals(lambda_xgc)
        goal2CPen = -1.0 * conceding23
        goal4CPen = -2.0 * conceding45

        return ((clean_sheet_points + goal_points + assist_points + appearance_points + goal2CPen + goal4CPen + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_midfielder_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        appearance_points = player["expected_minutes"] / 90
        TeamXGC90 = player["TeamXGC90"]
        opponent_xg90 = opponent.get("TeamXG90")
        reversecoeff = 2 - home_away_coefficient
        team_def_coeff = player["TeamDefCoef"]
        opponent_att_coeff = opponent.get("TeamAttCoef")
        opponent_def_coeff = opponent.get("TeamDefCoef")
        lambda_xgc = ((TeamXGC90*1/opponent_att_coeff + opponent_xg90*team_def_coeff) * reversecoeff) / 2
        clean_sheet_probability = poisson_cleansheet(lambda_xgc)
        clean_sheet_points = clean_sheet_probability * 1.0
        goal_points = player["xG90"] * 5.5 * opponent_def_coeff * home_away_coefficient
        assist_points = player["xA90"] * 3.15 * opponent_def_coeff * home_away_coefficient
        return ((clean_sheet_points + goal_points + assist_points + appearance_points + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_forward_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        appearance_points = player["expected_minutes"] / 90
        opponent_def_coeff = opponent.get("TeamDefCoef")
        goal_points = player["xG90"] * 4.4 * opponent_def_coeff * home_away_coefficient
        assist_points = player["xA90"] * 3.15 * opponent_def_coeff * home_away_coefficient
        return ((goal_points + assist_points + appearance_points + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

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
            probability = fixture["Probability"]

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

                # Adjust points based on the position and fixture details
                adj_points = 0
                fix_prob = probability

                # Handle potential zero coefficients
                if is_home:
                    is_home = home_coefficient
                else:
                    is_home = away_coefficient

                opponent_team = opponent_team
                opponent_data = {
                    "team_name": opponent_team,
                    "TeamXG90": team_xg90.get(opponent_team, 1),
                    "TeamXGC90": team_xgc90.get(opponent_team, 1),
                    "TeamAttCoef": team_coef_Att.get(opponent_team, 1),
                    "TeamDefCoef": team_coef_Def.get(opponent_team, 1)
                }

                if player["position"] == 1:  # Goalkeeper
                    adj_points = round(calculate_goalkeeper_value(player, opponent_data, is_home, fix_prob), 2)
                elif player["position"] == 2:  # Defender
                    adj_points = round(calculate_defender_value(player, opponent_data, is_home, fix_prob), 2)
                elif player["position"] == 3:  # Midfielder
                    adj_points = round(calculate_midfielder_value(player, opponent_data, is_home, fix_prob), 2)
                elif player["position"] == 4:  # Forward
                    adj_points = round(calculate_forward_value(player, opponent_data, is_home, fix_prob), 2)

                adjusted_points_dict[player["id"]][f"GW{gw}"] += adj_points

    return adjusted_points_dict


# Combine player data with calculated gameweek values and adjusted points
formatted_combined_player_data = []
start_gw = 1  # starting gameweek
end_gw = 27    # ending gameweek

# Step 1: Calculate adjusted points
for player in players_data:
    player_data = {
        "id": player["id"],
        "name": player["web_name"],
        "position": player["position"],
        "team": team_mappings.get(player["team"], "Unknown"),
        "price": player["cost"]
    }

    # Step 2: Calculate adjusted points for all gameweeks
    adjusted_points = calculate_adjusted_points([player], fixtures_data, start_gw, end_gw)
    player_data.update(adjusted_points.get(player["id"], {}))

    formatted_combined_player_data.append(player_data)

# Write to final_player_data.py
output_file_path = 'final_player_data.py'
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write("player_gameweek_data = [\n")
    for player in formatted_combined_player_data:
        f.write(f"    {json.dumps(player, ensure_ascii=False)},\n")
    f.write("]\n")

print(f"Player data saved to '{output_file_path}'")