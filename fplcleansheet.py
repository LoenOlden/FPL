import math
from scipy.stats import poisson

def poisson_cleansheet(lambda_xgc):
    prob_0 = poisson.pmf(0, lambda_xgc)
    return prob_0

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

lambda_xgc = 1.90
avgS = 4.25
csP = poisson_cleansheet(lambda_xgc)
xgc23 = poisson_probability_conceding_2_or_3_goals(lambda_xgc)
xgc45 = poisson_probability_conceding_4_or_5_goals(lambda_xgc)
shots3 = poisson_probability_3SHOTS(avgS)
shots6 = poisson_probability_6SHOTS(avgS)

output = (
    f'"csP": {csP:.3f}, '
    f'"xgc23": {xgc23:.3f}, '
    f'"xgc45": {xgc45:.3f}, '
    f'"3shots": {shots3:.3f}, '
    f'"6shots": {shots6:.3f}'
)
print(output)

"""
LIV 1.03*0.75 + 1.23*0.25 = 1.08
ARS 1.18*0.75 + 0.83*0.25 = 1.09
MCI 1.29*0.75 + 0.95*0.25 = 1.205
NFO 1.25*0.75 + 1.47*0.25 = 1.305
FUL 1.20*0.75 + 1.66*0.25 = 1.315
TOT 1.27*0.75 + 1.61*0.25 = 1.355
AVL 1.33*0.75 + 1.56*0.25 = 1.388
CHE 1.39*0.75 + 1.56*0.25 = 1.433
BOU 1.43*0.75 + 1.60*0.25 = 1.473
NEW 1.47*0.75 + 1.59*0.25 = 1.50
EVE 1.52*0.75 + 1.50*0.25 = 1.515
BHA 1.58*0.75 + 1.46*0.25 = 1.55
MUN 1.53*0.75 + 1.84*0.25 = 1.608
CRY 1.67*0.75 + 1.43*0.25 = 1.61
BRE 1.80*0.75 + 1.56*0.25 = 1.74
WHU 1.73*0.75 + 1.92*0.25 = 1.778
WOL 1.77*0.75 + 1.81*0.25 = 1.78
LEI 2.02*0.75 + 2.02*0.25 = 2.02
IPS 2.05*0.75 + 2.05*0.25 = 2.05
SOU 2.10*0.75 + 2.10*0.25 = 2.10

avgSave
LIV 2.67*0.75 + 2.84*0.25 = 2.71
ARS 2.83*0.75 + 1.42*0.25 = 2.48
MCI 2.25*0.75 + 2.00*0.25 = 2.19
NFO 2.75*0.75 + 2.58*0.25 = 2.71
FUL 2.83*0.75 + 3.50*0.25 = 3.00
TOT 2.33*0.75 + 2.87*0.25 = 2.47
AVL 2.42*0.75 + 3.03*0.25 = 2.57
CHE 3.33*0.75 + 3.29*0.25 = 3.32
BOU 3.92*0.75 + 3.34*0.25 = 3.78
NEW 3.83*0.75 + 3.50*0.25 = 3.75
EVE 2.58*0.75 + 3.08*0.25 = 2.71
BHA 3.33*0.75 + 2.76*0.25 = 3.19
MUN 2.67*0.75 + 3.84*0.25 = 2.96
CRY 3.33*0.75 + 2.58*0.25 = 3.14
BRE 5.00*0.75 + 3.13*0.25 = 4.53
WHU 2.83*0.75 + 4.45*0.25 = 3.24
WOL 3.33*0.75 + 3.66*0.25 = 3.41
LEI 3.83*0.75 + 3.83*0.25 = 3.83
IPS 3.83*0.75 + 3.83*0.25 = 3.83
SOU 4.25*0.75 + 4.25*0.25 = 4.25

team xGC90 avgSave CSP 23goal 45goal 3shots 6shots
LIV 1.08 2.71 "csP": 0.340, "xgc23": 0.269, "xgc45": 0.023, "3shots": 0.451, "6shots": 0.056
ARS 1.09 2.48 "csP": 0.336, "xgc23": 0.272, "xgc45": 0.024, "3shots": 0.410, "6shots": 0.040
MCI 1.205 2.19 "csP": 0.300, "xgc23": 0.305, "xgc45": 0.033, "3shots": 0.350, "6shots": 0.024
NFO 1.305 2.71 "csP": 0.271, "xgc23": 0.331, "xgc45": 0.041, "3shots": 0.451, "6shots": 0.056
FUL 1.315 3.00 "csP": 0.268, "xgc23": 0.334, "xgc45": 0.042, "3shots": 0.493, "6shots": 0.080
TOT 1.355 2.47 "csP": 0.258, "xgc23": 0.344, "xgc45": 0.046, "3shots": 0.408, "6shots": 0.039
AVL 1.388 2.57 "csP": 0.250, "xgc23": 0.352, "xgc45": 0.049, "3shots": 0.427, "6shots": 0.045
CHE 1.433 3.32 "csP": 0.239, "xgc23": 0.362, "xgc45": 0.054, "3shots": 0.525, "6shots": 0.112
BOU 1.473 3.78 "csP": 0.229, "xgc23": 0.371, "xgc45": 0.058, "3shots": 0.546, "6shots": 0.166
NEW 1.50 3.75 "csP": 0.223, "xgc23": 0.377, "xgc45": 0.061, "3shots": 0.546, "6shots": 0.162
EVE 1.515 2.71 "csP": 0.220, "xgc23": 0.380, "xgc45": 0.063, "3shots": 0.451, "6shots": 0.056
BHA 1.55 3.19 "csP": 0.212, "xgc23": 0.387, "xgc45": 0.067, "3shots": 0.514, "6shots": 0.099
MUN 1.608 2.96 "csP": 0.201, "xgc23": 0.397, "xgc45": 0.073, "3shots": 0.488, "6shots": 0.076
CRY 1.61 3.14 "csP": 0.200, "xgc23": 0.398, "xgc45": 0.074, "3shots": 0.509, "6shots": 0.094
BRE 1.74 4.53 "csP": 0.176, "xgc23": 0.420, "xgc45": 0.090, "3shots": 0.528, "6shots": 0.261
WHU 1.778 3.24 "csP": 0.169, "xgc23": 0.425, "xgc45": 0.095, "3shots": 0.518, "6shots": 0.104
WOL 1.78 3.41 "csP": 0.168, "xgc23": 0.426, "xgc45": 0.096, "3shots": 0.531, "6shots": 0.122
LEI 2.02 3.83 "csP": 0.133, "xgc23": 0.453, "xgc45": 0.129, "3shots": 0.547, "6shots": 0.172
IPS 2.05 3.83 "csP": 0.129, "xgc23": 0.455, "xgc45": 0.134, "3shots": 0.547, "6shots": 0.172
SOU 2.10 4.25 "csP": 0.122, "xgc23": 0.459, "xgc45": 0.141, "3shots": 0.541, "6shots": 0.225
"""
