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

def poisson_probability_conceding_6_or_more_goals(lambda_xgc):
    prob = 1.0 - sum(poisson.pmf(k, lambda_xgc) for k in range(6))
    return prob

team_xg90 = 0.0
lambda_xgc = 1.05
saves = 0.0

x = poisson_probability_conceding_2_or_3_goals(lambda_xgc)
y = poisson_probability_conceding_4_or_5_goals(lambda_xgc)
z = poisson_probability_conceding_6_or_more_goals(lambda_xgc)

print(x)
print(y)
print(z)


"""
NEW
Understat last 11/12, fbref and footystats
xg, xgC, avgsave
ARS 1.61 0.93 2.26
LIV 2.09 0.99 2.27
MCI 1.82 1.19 2.41
EVE 1.23 1.27 2.88
FUL 1.31 1.27 2.82
CHE 1.75 1.29 3.03
MUN 1.32 1.39 2.67
BHA 1.70 1.40 2.33
AVL 1.61 1.40 2.59
BOU 1.77 1.41 3.45
WOL 1.25 1.44 2.61
CRY 1.60 1.44 2.76
NEW 1.73 1.45 3.12
TOT 1.65 1.52 3.03
WHU 1.24 1.53 3.30
BRE 1.52 1.55 4.03
NFO 1.24 1.60 3.24
IPS 1.02 2.01 3.64
LEI 0.87 2.08 3.58
SOU 0.94 2.25 4.27


NEWS NEW 25/26
FBREF footystats understat XG
LIV 2.16 1.93 2.35 = 2.15
MCI 1.79 1.89 1.88 = 1.85
CHE 1.78 1.78 1.68 = 1.75
NEW 1.68 1.56 2.01 = 1.75
BOU 1.68 1.71 1.73 = 1.71
CRY 1.59 1.46 1.95 = 1.67
ARS 1.58 1.75 1.69 = 1.67
BRE 1.55 1.48 1.98 = 1.67
BHA 1.54 1.60 1.88 = 1.67
AVL 1.48 1.46 1.65 = 1.53
TOT 1.55 1.56 1.35 = 1.49
MUN 1.38 1.57 1.44 = 1.46
FUL 1.29 1.56 1.47 = 1.44
NFO 1.20 1.42 1.31 = 1.31
WOL 1.15 1.34 1.33 = 1.27
EVE 1.10 1.29 1.37 = 1.25
WHU 1.24 1.33 1.15 = 1.24
LEE 1.08 1.08 1.08 = 1.08
BUR 0.91 0.91 0.91 = 0.91
SUN 0.84 0.84 0.84 = 0.84
avg: 1.4855

XGC
ARS 0.91 1.10 1.12 = 1.04
LIV 1.02 1.26 1.21 = 1.16
MCI 1.26 1.12 1.15 = 1.18
CHE 1.24 1.27 1.26 = 1.26
EVE 1.22 1.53 1.16 = 1.30
FUL 1.24 1.39 1.33 = 1.32
NEW 1.20 1.46 1.38 = 1.35
BOU 1.28 1.48 1.41 = 1.39
AVL 1.32 1.45 1.39 = 1.39
CRY 1.29 1.47 1.43 = 1.40
BHA 1.44 1.27 1.51 = 1.41
MUN 1.42 1.33 1.56 = 1.44
WOL 1.53 1.51 1.50 = 1.51
BRE 1.46 1.84 1.39 = 1.56
NFO 1.29 1.68 1.74 = 1.57
WHU 1.57 1.68 1.48 = 1.58
BUR 1.62 1.62 1.62 = 1.62
TOT 1.67 1.56 1.89 = 1.71
LEE 2.11 2.11 2.11 = 2.11
SUN 2.61 2.61 2.61 = 2.61
avg 1.4955
"""