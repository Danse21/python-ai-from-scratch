# Bias in practice
# You are building an AI model to predict which patients have the highest
# risk of developing a disease, trained on historical care data.
# Two questions:
# 1. Name two specific types of bias that could enter the model from historical healthcare data,
#    and breifly explain where each comes from.
# 2. Name one concrete method you'd use to detect bias before the model goes into production.

# Question 1:
# Underrepresention bias:
# a. Certain age group and/or gender that were underdiagnosed in the passed will be missed by the model.
# b. Certain race that were understudied in the past will not be detected by the model giving a false negative result.

# Question 2:
# One concrete method:
# Disaggregated performance metrics: Instead of checking overall model accuracy (e.g., 90 % accurate),
# you split the test set by demographic group and measure accuracy per group:

for group in ["age_under_40", "age_under_70", "race_A", "race_B"]:
  subset = test_data[test_data["group"] == group]
  print(group, accuracy_score(subset["true"], subset["predicted"]))
