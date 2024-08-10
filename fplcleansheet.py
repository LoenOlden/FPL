import math
from scipy.stats import poisson

def poisson_probability_3SHOTS(avgS):
    prob_3 = poisson.pmf(3, avgS)
    prob_4 = poisson.pmf(4, avgS)
    prob_5 = poisson.pmf(5, avgS)
    prob_3shots = prob_3 + prob_4 + prob_5
    return prob_3shots

def poisson_probability_6SHOTS(avgS):
    prob_6 = poisson.pmf(6, avgS)
    prob_7 = poisson.pmf(7, avgS)
    prob_8 = poisson.pmf(8, avgS)
    prob_6shots = prob_6 + prob_7 + prob_8
    return prob_6shots

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

num = 146
avgS = num / 38
print(f"{poisson_probability_3SHOTS(avgS):.3f}")
print(f"{poisson_probability_6SHOTS(avgS):.3f}")

"""
xGA understat footystats fbref; csP, xgc23, xgc45, saves, 3shots, 6shots
ARS 0.84 0.92 0.73 = 0.83 = 0.436, 0.192, 0.01, 54, 0.168, 0.003
MCI 0.98 0.93 0.94 = 0.95 = 0.387, 0.230, 0.016, 76, 0.307, 0.016
LIV 1.25 1.23 1.20 = 1.23 = 0.292, 0.312, 0.035, 108, 0.472, 0.066
CRY 1.53 1.38 1.37 = 1.43 = 0.239, 0.361, 0.054, 98, 0.429, 0.046
BHA 1.60 1.33 1.46 = 1.46 = 0.232, 0.368, 0.057, 105, 0.460, 0.060
NFO 1.48 1.52 1.40 = 1.47 = 0.230, 0.370, 0.058, 98, 0.429, 0.046
EVE 1.59 1.47 1.45 = 1.50 = 0.223, 0.377, 0.061, 117, 0.502, 0.088
BRE 1.59 1.62 1.47 = 1.56 = 0.2102, 0.389, 0.068, 119, 0.508, 0.093
CHE 1.65 1.51 1.53 = 1.56 = 0.2101, 0.389, 0.068, 125, 0.523, 0.109
AVL 1.71 1.38 1.58 = 1.56 = 0.210, 0.389, 0.068, 115, 0.496, 0.083
NEW 1.64 1.51 1.62 = 1.59 = 0.204, 0.394, 0.072, 133, 0.537, 0.133
BOU 1.72 1.54 1.53 = 1.60 = 0.202, 0.396, 0.073, 127, 0.527, 0.115
TOT 1.79 1.38 1.67 = 1.61 = 0.200, 0.398, 0.074, 109, 0.475, 0.068
FUL 1.76 1.56 1.66 = 1.66 = 0.190, 0.407, 0.080, 133, 0.537, 0.133
WOL 2.00 1.65 1.78 = 1.81 = 0.164, 0.430, 0.100, 139, 0.543, 0.151
MUN 1.97 1.73 1.81 = 1.84 = 0.159, 0.434, 0.104, 146, 0.547, 0.174
WHU 2.05 1.85 1.87 = 1.92 = 0.147, 0.443, 0.115, 169, 0.532, 0.250
"""
"""
xGA understat footystats fbref; csP, xgc23, xgc45, 3shots, 6shots
ARS 0.84 0.92 0.73 = 0.83 = 0.436, 0.192, 0.01, 0.168, 0.003
AVL 1.71 1.38 1.58 = 1.56 = 0.210, 0.389, 0.068, 0.496, 0.083
BOU 1.72 1.54 1.53 = 1.60 = 0.202, 0.396, 0.073, 0.527, 0.115
BRE 1.59 1.62 1.47 = 1.56 = 0.2102, 0.389, 0.068, 0.508, 0.093
BHA 1.60 1.33 1.46 = 1.46 = 0.232, 0.368, 0.057, 0.460, 0.060
CHE 1.65 1.51 1.53 = 1.56 = 0.2101, 0.389, 0.068, 0.523, 0.109
CRY 1.53 1.38 1.37 = 1.43 = 0.239, 0.361, 0.054, 0.429, 0.046
EVE 1.59 1.47 1.45 = 1.50 = 0.223, 0.377, 0.061, 0.502, 0.088
FUL 1.76 1.56 1.66 = 1.66 = 0.190, 0.407, 0.080, 0.537, 0.133
IPS 0.00 0.00 0.00 = 1.92 = 0.147, 0.443, 0.115, 0.532, 0.250
LEI 0.00 0.00 0.00 = 1.92 = 0.147, 0.443, 0.115, 0.532, 0.250
LIV 1.25 1.23 1.20 = 1.23 = 0.292, 0.312, 0.035, 0.472, 0.066
MCI 0.98 0.93 0.94 = 0.95 = 0.387, 0.230, 0.016, 0.307, 0.016
MUN 1.97 1.73 1.81 = 1.84 = 0.159, 0.434, 0.104, 0.547, 0.174
NEW 1.64 1.51 1.62 = 1.59 = 0.204, 0.394, 0.072, 0.537, 0.133
NFO 1.48 1.52 1.40 = 1.47 = 0.230, 0.370, 0.058, 0.429, 0.046
SOU 0.00 0.00 0.00 = 1.92 = 0.147, 0.443, 0.115, 0.532, 0.250
TOT 1.79 1.38 1.67 = 1.61 = 0.200, 0.398, 0.074, 0.475, 0.068
WHU 2.05 1.85 1.87 = 1.92 = 0.147, 0.443, 0.115, 0.532, 0.250
WOL 2.00 1.65 1.78 = 1.81 = 0.164, 0.430, 0.100, 0.543, 0.151
"""

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

"""
Raya 5.5 0.436 
Ederson 5.5 0.387 
Alisson 5.5 0.292 
Johnstone80 4.5 0.239 
Verbruggen60 4.5 0.232 
Sels 4.5 0.230 
Pickford 5.0 0.223 
Flekken 4.5 0.210 
Sanchez80 4.5 0.210 
Martinez 5.0 0.210 
Pope 5.0 0.204 
Neto 4.5 0.202 
Vicario 5.0 0.190 
Leno 5.0 0.190 
Jose Sa 4.5 0.164 
Onana 5.0 0.159 
Areola 4.5 0.147 
"""
# Define defensive strengths using csP values
defensive_strength = {
    "ARS": 0.436,
    "MCI": 0.387,
    "LIV": 0.292,
    "CPA": 0.239,
    "BRI": 0.232,
    "NFO": 0.230,
    "EVE": 0.223,
    "BRE": 0.2102,
    "CHE": 0.2101,
    "AVL": 0.210,
    "NEW": 0.204,
    "BOU": 0.202,
    "TOT": 0.200,
    "FUL": 0.190,
    "WOL": 0.164,
    "MUN": 0.159,
    "WHU": 0.147,
    "LEI": 0.140,
    "IPS": 0.130,
    "SOU": 0.120
}

# Example csP values for teams (higher means stronger defense)
# Assuming team IDs from FPL API or any standard numbering
csP_values = {
    1: 0.436,  # Arsenal
    2: 0.210,  # Aston Villa
    3: 0.202,  # Bournemouth
    4: 0.2102,  # Brentford
    5: 0.232,  # Brighton
    6: 0.2101,  # Chelsea
    7: 0.239,  # Crystal Palace
    8: 0.223,  # Everton
    9: 0.190,  # Fulham
    10: 0.292,  # Liverpool
    11: 0.387,  # Manchester City
    12: 0.159,  # Manchester United
    13: 0.230,  # Nottingham Forest
    14: 0.140,  # Leicester
    15: 0.204,  # Newcastle
    16: 0.200,  # Tottenham
    17: 0.164,  # Wolves
    18: 0.147,  # West Ham
    19: 0.130,  # Ipswich
    20: 0.120  # Southampton
}