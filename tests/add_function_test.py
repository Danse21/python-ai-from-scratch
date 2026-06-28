# Write three unit tests (tests that test one function in isolation. No database, no files, no network required)

import pytest
from Module_4.add_function import add
# test one normal case
def test_all_positive_integer():
  """Normal positive numbers return a positive integer"""
  assert add(5, 5) == 10

# test one with negative numbers
def test_negative_numbers():
  """Negative numbers return a negaive integer"""
  assert add(-5, -5) == -10

# Test where one of the numbers is a float
def test_add_integer_with_float():
  """Adding an integer with a float returns a float"""
  assert add(5, 5.001) == pytest.approx(10.001)
