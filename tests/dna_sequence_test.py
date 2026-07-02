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
