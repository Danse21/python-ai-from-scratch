import pytest
from Module_4.calculate_base_content import calculate_gc_content

def test_known_DNA_string_calculate_expected_GC_content():
  """Given a known DNA string conataining GC% calculated as expected"""
  assert calculate_gc_content("AGCTTTTCATTCTGACTGCA") == 40.0

def test_empty_string_raises_error():
  """Invalid empty string raises ValueError"""
  with pytest.raises(ValueError):
    calculate_gc_content("")

def test_DNA_string_with_invalid_character_raises_error():
  """Invalid character in the DNA string raises ValueError"""
  with pytest.raises(ValueError):
    calculate_gc_content("AGCTTTTCATTCXGACTGCA")

def test_DNA_string_with_all_GC_return_100_percent():
  """Input DNA string containing only GC bases gives 100.0 percent"""
  assert calculate_gc_content("GGCGGCGGCGCC") == 100.0
