from scipy.stats import poisson

lambda_ = 14.4
p_ge_10 = 1 - poisson.cdf(11, mu=lambda_)

p_ge_10 = round(p_ge_10, 4)
expected_bonus_points = round(p_ge_10 * 2, 4)

print(p_ge_10)
print(expected_bonus_points)
