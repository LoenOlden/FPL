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
    1: 'ARS', 2: 'AVL', 3: 'BUR', 4: 'BOU', 5: 'BRE',
    6: 'BHA', 7: 'CHE', 8: 'CRY', 9: 'EVE', 10: 'FUL',
    11: 'LEE', 12: 'LIV', 13: 'MCI', 14: 'MUN', 15: 'NEW',
    16: 'NFO', 17: 'SUN', 18: 'TOT', 19: 'WHU', 20: 'WOL',
}

league_rankings = {
    "LIV": 1, "ARS": 2, "NEW": 3, "MCI": 4, "CHE": 5,
    "AVL": 6, "NFO": 7, "BRE": 8, "BHA": 9, "BOU": 10,
    "FUL": 11, "CRY": 12, "EVE": 13, "WOL": 14, "WHU": 15,
    "MUN": 16, "TOT": 17, "BUR": 18, "LEE": 19, "SUN": 20,
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

cbit_againstlasts = {
    "NFO": 6.35, "AVL": 6.53, "CRY": 6.60, "CHE": 6.68, "MUN": 6.88,
    "WHU": 6.88, "MCI": 6.95, "FUL": 7.0, "NEW": 7.0, "WOL": 7.15,
    "BRE": 7.20, "BOU": 7.35, "ARS": 7.35, "TOT": 7.60, "EVE": 7.83,
    "BHA": 7.88, "LIV": 8.58,
}

cbit_against = {
    "LIV": 1.213, "BHA": 1.083, "BOU": 1.053, "MCI": 1.048, "ARS": 1.046,
    "BRE": 1.036, "NEW": 1.035, "TOT": 1.033, "CHE": 1.013, "EVE": 1.009,
    "CRY": 0.994, "FUL": 0.983, "MUN": 0.978, "WOL": 0.966, "AVL": 0.965,
    "WHU": 0.941, "LEE": 0.933, "NFO": 0.916, "BUR": 0.888, "SUN": 0.869,
}

team_names_to_abbr = {
    'Arsenal': 'ARS', 'Aston Villa': 'AVL', 'Bournemouth': 'BOU', 'Brentford': 'BRE', 'Brighton': 'BHA',
    'Burnley': 'BUR', 'Chelsea': 'CHE', 'Crystal Palace': 'CRY', 'Everton': 'EVE', 'Fulham': 'FUL',
    'Leeds': 'LEE', 'Liverpool': 'LIV', 'Man City': 'MCI', 'Man Utd': 'MUN', 'Newcastle': 'NEW',
    'Nott\'m Forest': 'NFO', 'Sunderland': 'SUN', 'Spurs': 'TOT', 'West Ham': 'WHU', 'Wolves': 'WOL'
}

position_mapping = {
    1: 'G',
    2: 'D',
    3: 'M',
    4: 'F',
    5: 'AM'
}

home_coefficient = 1.114
away_coefficient = 0.886

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

def poisson_probability_conceding_6_or_more_goals(lambda_xgc):
    prob = 1.0 - sum(poisson.pmf(k, lambda_xgc) for k in range(6))
    return prob

def cbit_def(lambda_cbit):
    cbit_10 = 1 - poisson.cdf(9, mu=lambda_cbit)
    return cbit_10

def cbitr_midfwd(lambda_cbitr):
    cbitr_12 = 1 - poisson.cdf(11, mu=lambda_cbitr)
    return cbitr_12

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
        lambda_xgc = ((TeamXGC90*opponent_att_coeff + opponent_xg90*team_def_coeff) * reversecoeff) / 2
        clean_sheet_probability = poisson_cleansheet(lambda_xgc)
        clean_sheet_points = 4.16 * clean_sheet_probability
        conceding23 = poisson_probability_conceding_2_or_3_goals(lambda_xgc)
        conceding45 = poisson_probability_conceding_4_or_5_goals(lambda_xgc)
        conceding6more = poisson_probability_conceding_6_or_more_goals(lambda_xgc)
        
        offence_strength = get_opponent_offence_strength(opponent["team_name"])
        save_3points = 1.0 * player["3shots"] * offence_strength * reversecoeff
        save_6points = 2.0 * player["6shots"] * offence_strength * reversecoeff
        save_points = save_3points + save_6points
        goal2CPen = -1.0 * conceding23
        goal4CPen = -2.0 * conceding45
        goal6CPen = -3.0 * conceding6more
        goalPen = goal2CPen + goal4CPen + goal6CPen
        return ((clean_sheet_points + save_points + appearance_points + goalPen + 1) * appearance_points) * fix_prob
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
        lambda_xgc = ((TeamXGC90*opponent_att_coeff + opponent_xg90*team_def_coeff) * reversecoeff) / 2
        clean_sheet_probability = poisson_cleansheet(lambda_xgc)
        clean_sheet_points = 4.16 * clean_sheet_probability

        defense_strength = get_opponent_defense_strength(opponent["team_name"])
        goal_points = player["xG90"] * 6.24 * defense_strength * home_away_coefficient
        assist_points = player["xA90"] * 3.09 * defense_strength * home_away_coefficient

        conceding23 = poisson_probability_conceding_2_or_3_goals(lambda_xgc)
        conceding45 = poisson_probability_conceding_4_or_5_goals(lambda_xgc)
        conceding6more = poisson_probability_conceding_6_or_more_goals(lambda_xgc)
        goal2CPen = -1.0 * conceding23
        goal4CPen = -2.0 * conceding45
        goal6CPen = -3.0 * conceding6more
        goalPen = goal2CPen + goal4CPen + goal6CPen

        new_coef = (reversecoeff + 1.0)/2
        opponent_cbit = cbit_against.get(opponent["team_name"], 1.0)
        cbit90 = player["CBIT90"] * opponent_cbit * new_coef
        cbit_points = 2.0 * cbit_def(cbit90)
        
        return ((clean_sheet_points + goal_points + assist_points + appearance_points + goalPen + cbit_points + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_midfielder_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        appearance_points = player["expected_minutes"] / 93
        TeamXGC90 = player["TeamXGC90"]
        opponent_xg90 = opponent.get("TeamXG90")
        reversecoeff = 2 - home_away_coefficient
        team_def_coeff = player["TeamDefCoef"]
        opponent_att_coeff = opponent.get("TeamAttCoef")
        opponent_def_coeff = opponent.get("TeamDefCoef")
        
        lambda_xgc = ((TeamXGC90*opponent_att_coeff + opponent_xg90*team_def_coeff) * reversecoeff) / 2
        clean_sheet_probability = poisson_cleansheet(lambda_xgc)
        clean_sheet_points = clean_sheet_probability * 1.0
        
        goal_points = player["xG90"] * 5.3 * opponent_def_coeff * home_away_coefficient
        assist_points = player["xA90"] * 3.09 * opponent_def_coeff * home_away_coefficient
        
        new_coef = (reversecoeff + 1.0)/2
        opponent_cbit = cbit_against.get(opponent["team_name"], 1.0)
        cbitr90 = player["CBITR90"] * opponent_cbit * new_coef
        cbitr_points = 2.0 * cbitr_midfwd(cbitr90)
        
        """if player["web_name"] == 'Wirtz':
            print(
                f"opp: {opponent.get('team_name')}, "
                f"oppCBITagainst: {cbit_against.get(opponent['team_name'])}, "
                f"CBITRthis: {cbitr90:.3f}, "
                f"CBIT Points: {cbitr_points:.3f}"
            )"""

        return ((clean_sheet_points + goal_points + assist_points + appearance_points + cbitr_points + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

def calculate_forward_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        appearance_points = player["expected_minutes"] / 93
        opponent_def_coeff = opponent.get("TeamDefCoef")
        goal_points = player["xG90"] * 4.32 * opponent_def_coeff * home_away_coefficient
        assist_points = player["xA90"] * 3.09 * opponent_def_coeff * home_away_coefficient
        
        reversecoeff = 2 - home_away_coefficient
        new_coef = (reversecoeff + 1.0)/2
        opponent_cbit = cbit_against.get(opponent["team_name"], 1.0)
        cbitr90 = player["CBITR90"] * opponent_cbit * new_coef
        cbitr_points = 2.0 * cbitr_midfwd(cbitr90)
        
        return ((goal_points + assist_points + appearance_points + cbitr_points + 1) * appearance_points) * fix_prob
    except KeyError as e:
        print(f"KeyError: {e} - Missing in player data: {player}")
        return 0

"""def calculate_manager_value(player, opponent, home_away_coefficient, fix_prob):
    try:
        # RULES
        # win = 6
        # draw = 3
        # goal scored = 1
        # clean sheet = 2
        # tablebonus(D) = 5
        # tablebonus(W) = 10
        
        # Extracting player and opponent stats
        TeamXGC90 = player["TeamXGC90"]
        TeamXG90 = player["TeamXG90"]
        opponent_xg90 = opponent.get("TeamXG90")
        opponent_xgc90 = opponent.get("TeamXGC90")
        reversecoeff = 2 - home_away_coefficient
        team_def_coeff = player["TeamDefCoef"]
        team_att_coeff = player["TeamAttCoef"]
        opponent_att_coeff = opponent.get("TeamAttCoef")
        opponent_def_coeff = opponent.get("TeamDefCoef")
        
        # Calculating expected goals (xG) and expected goals conceded (xGC)
        lambda_xgc = (((TeamXGC90 * opponent_att_coeff + opponent_xg90 * team_def_coeff)) / 2) * reversecoeff
        lambda_xg = (((TeamXG90 * opponent_def_coeff + opponent_xgc90 * team_att_coeff)) / 2) * home_away_coefficient

        # Cleansheet probability
        def cleansheet(lambda_xgc):
            return poisson.pmf(0, lambda_xgc)

        # Scoring probabilities for the team
        def teamscore0(lambda_xg): return poisson.pmf(0, lambda_xg)
        def teamscore1(lambda_xg): return poisson.pmf(1, lambda_xg)
        def teamscore2(lambda_xg): return poisson.pmf(2, lambda_xg)
        def teamscore3(lambda_xg): return poisson.pmf(3, lambda_xg)
        def teamscore4(lambda_xg): return poisson.pmf(4, lambda_xg)
        def teamscore5(lambda_xg): return poisson.pmf(5, lambda_xg)
        def teamscore6(lambda_xg): return poisson.pmf(6, lambda_xg)
        def teamscore7(lambda_xg): return poisson.pmf(7, lambda_xg)

        # Scoring probabilities for the opponent
        def opponentscore0(lambda_xgc): return poisson.pmf(0, lambda_xgc)
        def opponentscore1(lambda_xgc): return poisson.pmf(1, lambda_xgc)
        def opponentscore2(lambda_xgc): return poisson.pmf(2, lambda_xgc)
        def opponentscore3(lambda_xgc): return poisson.pmf(3, lambda_xgc)
        def opponentscore4(lambda_xgc): return poisson.pmf(4, lambda_xgc)
        def opponentscore5(lambda_xgc): return poisson.pmf(5, lambda_xgc)
        def opponentscore6(lambda_xgc): return poisson.pmf(6, lambda_xgc)
        def opponentscore7(lambda_xgc): return poisson.pmf(7, lambda_xgc)

        # Cumulative scores for team and opponent
        def teamcumulativescore0(lambda_xg): return teamscore0(lambda_xg)
        def teamcumulativescore1(lambda_xg): return teamscore0(lambda_xg) + teamscore1(lambda_xg)
        def teamcumulativescore2(lambda_xg): return teamscore0(lambda_xg) + teamscore1(lambda_xg) + teamscore2(lambda_xg)
        def teamcumulativescore3(lambda_xg): return teamscore0(lambda_xg) + teamscore1(lambda_xg) + teamscore2(lambda_xg) + teamscore3(lambda_xg)
        def teamcumulativescore4(lambda_xg): return teamscore0(lambda_xg) + teamscore1(lambda_xg) + teamscore2(lambda_xg) + teamscore3(lambda_xg) + teamscore4(lambda_xg)
        def teamcumulativescore5(lambda_xg): return teamscore0(lambda_xg) + teamscore1(lambda_xg) + teamscore2(lambda_xg) + teamscore3(lambda_xg) + teamscore4(lambda_xg) + teamscore5(lambda_xg)
        def teamcumulativescore6(lambda_xg): return teamscore0(lambda_xg) + teamscore1(lambda_xg) + teamscore2(lambda_xg) + teamscore3(lambda_xg) + teamscore4(lambda_xg) + teamscore5(lambda_xg) + teamscore6(lambda_xg)

        def opponentcumulativescore0(lambda_xgc): return opponentscore0(lambda_xgc)
        def opponentcumulativescore1(lambda_xgc): return opponentscore0(lambda_xgc) + opponentscore1(lambda_xgc)
        def opponentcumulativescore2(lambda_xgc): return opponentscore0(lambda_xgc) + opponentscore1(lambda_xgc) + opponentscore2(lambda_xgc)
        def opponentcumulativescore3(lambda_xgc): return opponentscore0(lambda_xgc) + opponentscore1(lambda_xgc) + opponentscore2(lambda_xgc) + opponentscore3(lambda_xgc)
        def opponentcumulativescore4(lambda_xgc): return opponentscore0(lambda_xgc) + opponentscore1(lambda_xgc) + opponentscore2(lambda_xgc) + opponentscore3(lambda_xgc) + opponentscore4(lambda_xgc)
        def opponentcumulativescore5(lambda_xgc): return opponentscore0(lambda_xgc) + opponentscore1(lambda_xgc) + opponentscore2(lambda_xgc) + opponentscore3(lambda_xgc) + opponentscore4(lambda_xgc) + opponentscore5(lambda_xgc)
        def opponentcumulativescore6(lambda_xgc): return opponentscore0(lambda_xgc) + opponentscore1(lambda_xgc) + opponentscore2(lambda_xgc) + opponentscore3(lambda_xgc) + opponentscore4(lambda_xgc) + opponentscore5(lambda_xgc) + opponentscore6(lambda_xgc)

        # Win probability
        def winprobability(lambda_xg, lambda_xgc):
            withonegoal = teamscore1(lambda_xg) * opponentcumulativescore0(lambda_xgc)
            withtwogoal = teamscore2(lambda_xg) * opponentcumulativescore1(lambda_xgc)
            withthreegoal = teamscore3(lambda_xg) * opponentcumulativescore2(lambda_xgc)
            withfourgoal = teamscore4(lambda_xg) * opponentcumulativescore3(lambda_xgc)
            withfivegoal = teamscore5(lambda_xg) * opponentcumulativescore4(lambda_xgc)
            withsixgoal = teamscore6(lambda_xg) * opponentcumulativescore5(lambda_xgc)
            withsevengoal = teamscore7(lambda_xg) * opponentcumulativescore6(lambda_xgc)
            return withonegoal + withtwogoal + withthreegoal + withfourgoal + withfivegoal + withsixgoal + withsevengoal

        # Draw probability
        def drawprobability(lambda_xg, lambda_xgc):
            zerozero = teamscore0(lambda_xg) * opponentscore0(lambda_xgc)
            oneone = teamscore1(lambda_xg) * opponentscore1(lambda_xgc)
            twotwo = teamscore2(lambda_xg) * opponentscore2(lambda_xgc)
            threethree = teamscore3(lambda_xg) * opponentscore3(lambda_xgc)
            fourfour = teamscore4(lambda_xg) * opponentscore4(lambda_xgc)
            fivefive = teamscore5(lambda_xg) * opponentscore5(lambda_xgc)
            sixsix = teamscore6(lambda_xg) * opponentscore6(lambda_xgc)
            sevenseven = teamscore7(lambda_xg) * opponentscore7(lambda_xgc)
            return zerozero + oneone + twotwo + threethree + fourfour + fivefive + sixsix + sevenseven

        # Loss probability
        def loseprobability(lambda_xg, lambda_xgc):
            withonegoal = opponentscore1(lambda_xgc) * teamcumulativescore0(lambda_xg)
            withtwogoal = opponentscore2(lambda_xgc) * teamcumulativescore1(lambda_xg)
            withthreegoal = opponentscore3(lambda_xgc) * teamcumulativescore2(lambda_xg)
            withfourgoal = opponentscore4(lambda_xgc) * teamcumulativescore3(lambda_xg)
            withfivegoal = opponentscore5(lambda_xgc) * teamcumulativescore4(lambda_xg)
            withsixgoal = opponentscore6(lambda_xgc) * teamcumulativescore5(lambda_xg)
            withsevengoal = opponentscore7(lambda_xgc) * teamcumulativescore6(lambda_xg)
            return withonegoal + withtwogoal + withthreegoal + withfourgoal + withfivegoal + withsixgoal + withsevengoal

        def tablebase(player, opponent):
            team_id = player["team"]
            team_abbr = team_mappings.get(team_id)
            league_ranking = league_rankings.get(team_abbr)
            opponent_ranking = league_rankings.get(opponent.get("team"))
            
            if league_ranking and opponent_ranking:  # Ensure both rankings exist
                if (league_ranking - opponent_ranking >= 5):
                    return win_prob, draw_prob
                else:
                    return 0, 0  # Return a tuple, not a single int value
            else:
                return 0, 0  # Handle the case where the rankings are missing
            
        win_prob = winprobability(lambda_xg, lambda_xgc)
        draw_prob = drawprobability(lambda_xg, lambda_xgc)
        # lose_prob = loseprobability(lambda_xg, lambda_xgc)
        tablewin_prob, tabledraw_prob = tablebase(player, opponent)

        win_points = win_prob * 6
        draw_points = draw_prob * 3
        goal_points = lambda_xg
        cs_points = cleansheet(lambda_xgc) * 2
        tablewin_points = tablewin_prob * 10
        tabledraw_points = tabledraw_prob * 5

        # Total manager value
        manager_value = win_points + draw_points + goal_points + cs_points + tablewin_points + tabledraw_points

        # Adjust with fix probability if relevant
        manager_value *= fix_prob

        return manager_value

    except KeyError as e:
        print(f"Error: {str(e)}")
        return None
    except Exception as e:
        print("Error calculating manager value:", e)
        return None
"""

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
                    "team": opponent_team,
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
                """elif player["position"] == 5:  # Manager
                    adj_points = round(calculate_manager_value(player, opponent_data, is_home, fix_prob), 2)"""

                adjusted_points_dict[player["id"]][f"GW{gw}"] += round(adj_points, 2)

    return adjusted_points_dict

# Combine player data with calculated gameweek values and adjusted points
formatted_combined_player_data = []
start_gw = 1  # starting gameweek
end_gw = 12    # ending gameweek

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