class DNASequence:
  def __init__(self, sample_id: str, sequence: str):
    self.sample_id = sample_id
    self.sequence = sequence

  def get_length(self) -> int:
    return len(self.sequence)

  def __str__(self) -> str:
    """Used by print()"""
    return f"Sample {self.sample_id}: {self.sequence} ({self.get_length()} bases)"

S1 = DNASequence("P001", "AGCTTTTCA")
S2 = DNASequence("P002", "AGCTTTTCATTCTGACTGCAACGGGCAATA")

print(S1)
print(S2)
