# A unit test that raises ValueError when an invalid input is present

import pytest
from Module_4.count_dna3 import count_nucleotides

def test_raises_ValueError_with_invalid_character_input():
  """In the presence of invalid character input, raise ValueError"""
  with pytest.raises(ValueError):
   count_nucleotides("AGCTTTTCATTCXGACTGCA")

def test_raises_TypeError_with_invalid_data_type_input():
  """Raise TypeError when input data type is not a string"""
  with pytest.raises(TypeError):
    count_nucleotides(1234567890)
