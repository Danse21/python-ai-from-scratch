# Unit test for count_nucleotides

from Module_4.count_dna2 import count_nucleotide

def test_count_normal_dna_string():
  """Counting normal DNA string returns correct number of each nucleoside in the string"""
  assert count_nucleotide("AGCTTTTCATTCTGACTGCA") == (4, 5, 3, 8)

def test_count_empty_dna_string():
  """Counting empty DNA string returns 0"""
  assert count_nucleotide("") == (0, 0, 0, 0)

def test_count_single_base_character():
  """Counting a single character (one ebase) returns 1 at the exact position as ordered (A, C, G, T)"""
  assert count_nucleotide("T") == (0, 0, 0, 1)

def test_count_all_same_base_string():
  """Counting an all-base string returns the exact number of the base and
  at exact position as ordered (A, C, G, T)"""
  assert count_nucleotide("AAAA") == (4, 0, 0, 0)
