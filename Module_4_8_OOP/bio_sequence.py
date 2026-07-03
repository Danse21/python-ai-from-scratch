# Refactor using inheritance: create a base class BioSequence with common attributes
# (sequence, sample_id) and shared methods (__str__, __len__, __eq__).
# Then create two subclasses — DNASequence (adds gc_content()) and ProteinSequence
# (adds amino_acid_count() that returns the number of unique amino acids in
# the sequence). Use super() correctly.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Module_4.calculate_base_content import calculate_gc_content

class BioSequence:
  def __init__(self, sample_id: str, sequence: str):
    self.sample_id = sample_id
    self.sequence = sequence

  def __len__(self) -> int:
    # Validate that input is not empty string
    if len(self.sequence) == 0:
      raise ValueError(f"Invalid input: {self.sequence}")
    return len(self.sequence)

  def __eq__(self, other) -> bool:
    return self.sequence == other.sequence

  def __str__(self):
    return f"Sample: {self.sample_id}: {self.sequence} ({len(self)} bases)."

class DNASequence (BioSequence):
  def __init__(self, sample_id: str, sequence: str):
    super().__init__(sample_id, sequence)

  def gc_content(self) -> float:
    return calculate_gc_content(self.sequence)

  # Override BioSequence.__str__()
  def __str__(self):
    return f"Sample {self.sample_id}: {self.sequence} ({len(self)} bases, GC: {self.gc_content(): .1f}%)"

class ProteinSequence(BioSequence):
  def __init__(self, sample_id: str, sequence: str):
    super().__init__(sample_id, sequence)

  def amino_acid_count(self) -> int:
    # Count unique amino acids, set() removes duplicates
    return len(set(self.sequence))

  # Override BioSequence__str__()
  def __str__(self):
    return f"Sample {self.sample_id}: {self.sequence} ({self.amino_acid_count()} unique amino acids)"

if __name__ == "__main__":
  dna = DNASequence("P001", "AGCTTTTCA")
  protein = ProteinSequence("PR001", "ACDEFGHIKLMNPQRSTVWY")
  print(dna)
  print(protein)

