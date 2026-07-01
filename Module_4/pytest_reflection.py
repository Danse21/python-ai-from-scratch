# You have a function that reads patient data from a file and
# returns a risk score. Why can't you easily unit test it as-is?
# What would you change about the function's design to make it testable?

# original function
def get_patient_risk_score(patient_id):
  data = read_from_file(f"patients/{patient_id}.csv")
  score = run_model(data)
  return score

# You cannot easily unit test it as-is because of external dependencies
# What the function does:
data = read_from_file(f"patients/{patients_id}.csv")   # needs real files on disk
score = run_model(data)   # needs a real model loaded

# To run this function in a test, you'd need actual CSV files in a specific folder
# structure AND a working model. If the files don't exist, the test crashes —
# not because your logic is wrong, but because the environment isn't set up.
# That's not a unit test, it's an integration test.

# The fix is to separate concerns:
# Logic --> can be unit test by passing in dictionary directly - no file needed.
def calculate_risk_score(data: dict) -> float:
 score = run_model(data)
 return score

# Read file
def get_patient_risk_score(patient_id: str) -> float:
  data = read_from_file(f"patients/{patient_id}.csv")
  return calculate_risk_score(data)

# Test example
def test_high_risk_score():
  fake_data = {"age": 75, "biomarker_x": 9.2}
  assert calculate_risk_score(fake_data)

# Concluding statement:
# A unit test should never touch the file system, a database, or network.
# Only integration test does, that what differentiates the two.
# If your function does those things,
# split it so the pure logic can be unit tested in isolation
