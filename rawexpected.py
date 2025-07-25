import json
from updated_player_data import players_data
from scipy.stats import poisson

# Define position mappings
position_mapping = {
    1: 'Goalkeepers',
    2: 'Defenders',
    3: 'Midfielders',
    4: 'Forwards'
}

def cbit_def(lambda_cbit):
    cbit_10 = 1 - poisson.cdf(9, mu=lambda_cbit)
    return cbit_10

def cbitr_midfwd(lambda_cbitr):
    cbitr_12 = 1 - poisson.cdf(11, mu=lambda_cbitr)
    return cbitr_12

def calculate_goalkeeper_value(player):
    try:
        appearance_points = player["expected_minutes"] / 93
        clean_sheet_points = player["csP"] * 4.16
        save_3points = player["3shots"] * 1.0
        save_6points = player["6shots"] * 1.0
        save_points = save_3points + save_6points
        goal2CPen = -1.0 * (player["xgc23"])
        goal4CPen = -2.0 * (player["xgc45"])
        
        return (clean_sheet_points + save_points + appearance_points + goal2CPen + goal4CPen + 1) * appearance_points
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_defender_value(player):
    try:
        appearance_points = player["expected_minutes"] / 93
        clean_sheet_points = player["csP"] * 4.16
        goal_points = player["xG90"] * 6.24
        assist_points = player["xA90"] * 3.09
        goal2CPen = -1.0 * (player["xgc23"])
        goal4CPen = -2.0 * (player["xgc45"])
        cbit = 2 * cbit_def(player["CBIT90"])
        return (clean_sheet_points + goal_points + assist_points + appearance_points + goal2CPen + goal4CPen + cbit + 1) * appearance_points
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_midfielder_value(player):
    try:
        appearance_points = player["expected_minutes"] / 90
        clean_sheet_points = player["csP"] * 1
        goal_points = player["xG90"] * 5.3
        assist_points = player["xA90"] * 3.09
        cbit = 2 * cbitr_midfwd(player["CBITR90"])
        return (clean_sheet_points + goal_points + assist_points + appearance_points + cbit + 1) * appearance_points
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_forward_value(player):
    try:
        appearance_points = player["expected_minutes"] / 90
        goal_points = player["xG90"] * 4.32
        assist_points = player["xA90"] * 3.09
        cbit = 2 * cbitr_midfwd(player["CBITR90"])
        return (goal_points + assist_points + appearance_points + cbit + 1) * appearance_points
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def process_players(players, calculate_value_function):
    players_list = []
    for player in players:
        value = calculate_value_function(player)
        players_list.append({
            "id": player["id"],
            "name": player["web_name"],
            "position": player["position"],
            "team": player["team"],
            "cost": player["cost"],
            "xP": value
        })
    return sorted(players_list, key=lambda x: x["xP"], reverse=True)

# Filter players by position from players_data
goalkeepers = [player for player in players_data if player["position"] == 1]
defenders = [player for player in players_data if player["position"] == 2]
midfielders = [player for player in players_data if player["position"] == 3]
forwards = [player for player in players_data if player["position"] == 4]

# Process players for each position
goalkeepers_sorted = process_players(goalkeepers, calculate_goalkeeper_value)
defenders_sorted = process_players(defenders, calculate_defender_value)
midfielders_sorted = process_players(midfielders, calculate_midfielder_value)
forwards_sorted = process_players(forwards, calculate_forward_value)

# Prepare data for output
output_data = {
    "goalkeepers_sorted": goalkeepers_sorted,
    "defenders_sorted": defenders_sorted,
    "midfielders_sorted": midfielders_sorted,
    "forwards_sorted": forwards_sorted
}

# Write to a .py file with formatted output
output_file = "sorted_players_data.py"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("goalkeepers_sorted = [\n")
    for player in goalkeepers_sorted:
        file.write(f'    {{ "id": "{player["id"]}", "name": "{player["name"]}", "position": "{player["position"]}", "team": {player["team"]}, "cost": {player["cost"]}, "xP": {player["xP"]:.2f} }},\n')
    file.write("]\n\n")

    file.write("defenders_sorted = [\n")
    for player in defenders_sorted:
        file.write(f'    {{ "id": "{player["id"]}", "name": "{player["name"]}", "position": "{player["position"]}", "team": {player["team"]}, "cost": {player["cost"]}, "xP": {player["xP"]:.2f} }},\n')
    file.write("]\n\n")

    file.write("midfielders_sorted = [\n")
    for player in midfielders_sorted:
        file.write(f'    {{ "id": "{player["id"]}", "name": "{player["name"]}", "position": "{player["position"]}", "team": {player["team"]}, "cost": {player["cost"]}, "xP": {player["xP"]:.2f} }},\n')
    file.write("]\n\n")

    file.write("forwards_sorted = [\n")
    for player in forwards_sorted:
        file.write(f'    {{ "id": "{player["id"]}", "name": "{player["name"]}", "position": "{player["position"]}", "team": {player["team"]}, "cost": {player["cost"]}, "xP": {player["xP"]:.2f} }},\n')
    file.write("]\n")

print(f"Player data saved to '{output_file}'")