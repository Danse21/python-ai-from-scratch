import pytest
from Module_4_8_OOP.dna_sequence import DNASequence

def test_Invalid_input_data_raises_error():
  """Passing invalid input data type raises TypeError"""
  with pytest.raises(TypeError):
    DNASequence("P001", 1234567890)

def test_gc_content_return_correct_percentage():
  """With a given DNA sequence, correct GC content is calculated"""
  seq = DNASequence("P001", "AGCTTTTCATTCTGACC")
  assert seq.gc_content() == pytest.approx(41.18, rel=1e-2)

# Key lesson from this debugging session worth remembering:
# always create an instance before calling instance methods.
# DNASequence.gc_content() and seq.gc_content() look similar
# but are fundamentally different — the first passes nothing as self,
# the second passes the instance automatically.

def test_len_returns_number_of_sequence_content():
  """When len() function gives the correct number of sequence content"""
  dna = DNASequence("P002", "AGCTTTTCATTCTGACC")
  assert len(dna) == 17

def test_two_same_sequences_are_equal():
  """Two sequences are considered equal if their sequence strings match
    even they have different sample id"""
  seq1 = DNASequence("P003", "AGCTTTTCATTCTGACCTGCAACGGGCAATACCTC")
  seq2 = DNASequence("P004", "AGCTTTTCATTCTGACCTGCAACGGGCAATACCTC")
  assert seq1 == seq2

def test_two_different_sequences_are_not_equal():
  """Two sequences are considered equal if their sequence strings match
    even they have different sample id"""
  seq1 = DNASequence("P005", "AGCTTTTCATTCTGACCTGCAACGGGCAATACCTC")
  seq2 = DNASequence("P006", "AGCTTTTCATTCTGACCTGCAACGGGCAATACC")
  assert seq1 != seq2

# Dunder methods are meant to be invoked through the built-ins
# (len(), ==, print()), not called directly. The built-in does a bit more than
# just calling the method — it also does type checking and optimizations.
