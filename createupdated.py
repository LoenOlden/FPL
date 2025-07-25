import json
from scipy.stats import poisson
from updated_player_data import players_data

# === Poisson-based helper functions ===

def poisson_cleansheet(lambda_xgc):
    return poisson.pmf(0, lambda_xgc)

def poisson_probability_3SHOTS(avgS):
    return poisson.pmf(3, avgS) + poisson.pmf(4, avgS) + poisson.pmf(5, avgS)

def poisson_probability_6SHOTS(avgS):
    return poisson.pmf(6, avgS) + poisson.pmf(7, avgS) + poisson.pmf(8, avgS)

def poisson_probability_conceding_2_or_3_goals(lambda_xgc):
    return poisson.pmf(2, lambda_xgc) + poisson.pmf(3, lambda_xgc)

def poisson_probability_conceding_4_or_5_goals(lambda_xgc):
    return poisson.pmf(4, lambda_xgc) + poisson.pmf(5, lambda_xgc)

# === Static team data ===

team_mappings = {
    1: 'ARS', 2: 'AVL', 3: 'BUR', 4: 'BOU', 5: 'BRE',
    6: 'BHA', 7: 'CHE', 8: 'CRY', 9: 'EVE', 10: 'FUL',
    11: 'LEE', 12: 'LIV', 13: 'MCI', 14: 'MUN', 15: 'NEW',
    16: 'NFO', 17: 'SUN', 18: 'TOT', 19: 'WHU', 20: 'WOL',
}

team_coef_Att = {
    "LIV": 1.447, "MCI": 1.245, "CHE": 1.178, "NEW": 1.178, "BOU": 1.151,
    "CRY": 1.124, "ARS": 1.124, "BRE": 1.124, "BHA": 1.124, "AVL": 1.030,
    "TOT": 1.003, "MUN": 0.983, "FUL": 0.969, "NFO": 0.882, "WOL": 0.855,
    "EVE": 0.841, "WHU": 0.835, "LEE": 0.727, "BUR": 0.613, "SUN": 0.565,
}

team_coef_Def = {
    "ARS": 0.695, "LIV": 0.776, "MCI": 0.789, "CHE": 0.843, "EVE": 0.869,
    "FUL": 0.883, "NEW": 0.903, "BOU": 0.929, "AVL": 0.929, "CRY": 0.936,
    "BHA": 0.943, "MUN": 0.963, "WOL": 1.010, "BRE": 1.043, "NFO": 1.050,
    "WHU": 1.057, "BUR": 1.083, "TOT": 1.143, "LEE": 1.411, "SUN": 1.745,
}

team_xg90 = {
    "LIV": 2.15, "MCI": 1.85, "CHE": 1.75, "NEW": 1.75, "BOU": 1.71,
    "CRY": 1.67, "ARS": 1.67, "BRE": 1.67, "BHA": 1.67, "AVL": 1.53,
    "TOT": 1.49, "MUN": 1.46, "FUL": 1.44, "NFO": 1.31, "WOL": 1.27,
    "EVE": 1.25, "WHU": 1.24, "LEE": 1.08, "BUR": 0.91, "SUN": 0.84,
}

team_xgc90 = {
    "ARS": 1.04, "LIV": 1.16, "MCI": 1.18, "CHE": 1.26, "EVE": 1.30,
    "FUL": 1.32, "NEW": 1.35, "BOU": 1.39, "AVL": 1.39,  "CRY": 1.40,
    "BHA": 1.41, "MUN": 1.44, "WOL": 1.51,  "BRE": 1.56, "NFO": 1.57,
    "WHU": 1.58, "BUR": 1.62, "TOT": 1.71, "LEE": 2.11, "SUN": 2.61,
}

saves90 = {
    "MCI": 2.26, "ARS": 2.26, "BHA": 2.37, "MUN": 2.53, "LIV": 2.58,
    "WOL": 2.63, "CRY": 2.66, "AVL": 2.74, "FUL": 2.79, "CHE": 2.92,
    "NEW": 3.03, "EVE": 3.08, "TOT": 3.13, "NFO": 3.13, "BOU": 3.32,
    "WHU": 3.34, "LEE": 3.37, "BUR": 3.72, "SUN": 3.91, "BRE": 4.03,
}

# === Process and update player data ===

updated_players = []

for player in players_data:
    team_id = player["team"]
    team_abbr = team_mappings.get(team_id, "")
    xgc = team_xgc90.get(team_abbr, 0.0)
    sv90 = saves90.get(team_abbr, 0.0)

    updated_player = {
        "id": player["id"],
        "web_name": player["web_name"],
        "team": team_id,
        "position": player["position"],
        "cost": player["cost"],
        "minutes": player["minutes"],
        "saves90": sv90,
        "xG90": player["xG90"],
        "xA90": player["xA90"],
        "csP": round(poisson_cleansheet(xgc), 3),
        "xgc23": round(poisson_probability_conceding_2_or_3_goals(xgc), 3),
        "xgc45": round(poisson_probability_conceding_4_or_5_goals(xgc), 3),
        "3shots": round(poisson_probability_3SHOTS(sv90), 3),
        "6shots": round(poisson_probability_6SHOTS(sv90), 3),
        "TeamXG90": team_xg90.get(team_abbr, 0.0),
        "TeamXGC90": xgc,
        "TeamAttCoef": team_coef_Att.get(team_abbr, 0.0),
        "TeamDefCoef": team_coef_Def.get(team_abbr, 0.0),
        "CBIT90": player["CBIT90"],
        "CBITR90": player["CBITR90"],
        "expected_minutes": 0.0  # Placeholder
    }

    updated_players.append(updated_player)

# === Export to Python file ===

with open("updated_player_data3.py", "w", encoding="utf-8") as f:
    f.write("players_data = [\n")
    for player in updated_players:
        f.write(f"    {json.dumps(player, ensure_ascii=False)},\n")
    f.write("]\n")

