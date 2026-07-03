import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Module_4.calculate_base_content import calculate_gc_content
class DNASequence:
  def __init__(self, sample_id: str, sequence: str):
    # Validate input data type
    if not isinstance(sequence, str):
      raise TypeError(f"Expected string, got {type(sequence).__name__}")
    # Validate DNA bases
    for base in sequence:
      if base not in {"A", "C", "G", "T"}:
        raise ValueError(f"Invalid base: {base}")
    self.sample_id = sample_id
    self.sequence = sequence

  def __len__(self) -> int:
    return len(self.sequence)

  def __eq__(self, other) -> bool:
    return self.sequence == other.sequence

  def gc_content(self) -> float:
    return calculate_gc_content(self.sequence)


  def __str__(self) -> str:
    """Used by print()"""
    return f"Sample {self.sample_id}: {self.gc_content()} {self.sequence} ({len(self)} bases)"

if __name__ == "__main__":
  # S1 = DNASequence("P001", "AGCTTTTCA")
  S2 = DNASequence("P002", "AGCTTTTCATTCTGACCTGCAACGGGCAATACCTC")

  # print(S1)
  print(S2)

# Dunder methods are meant to be invoked through the built-ins
# (len(), ==, print()), not called directly. The built-in does a bit more than
# just calling the method — it also does type checking and optimizations.
# Python classes communicate with built-in operations through
# dunder (double underscore) methods: __len__(), __eq__(), __str__().
