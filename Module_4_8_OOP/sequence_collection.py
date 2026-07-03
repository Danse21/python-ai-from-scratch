# Create a SequenceCollection class that holds a list of DNASequence objects.
# Add methods: add_sequence(seq: DNASequence), get_by_id(sample_id: str) -> DNASequence,
# average_gc_content() -> float, and __len__.
# Handle the case where get_by_id finds no match.

from dna_sequence import DNASequence

class SequenceCollection:
  def __init__(self):
    self.dna_sequences = []

  def add_sequence(self, seq: DNASequence):
    self.dna_sequences.append(seq)

  def get_by_id(self, sample_id: str) -> DNASequence:
    # Loop through self.dna_sequences
    for dna_seq in self.dna_sequences:
      if dna_seq.sample_id == sample_id:
        return dna_seq
    return None     # No match found

  def __len__(self) -> int:
    return len(self.dna_sequences)

  def average_gc_content(self) -> float:
    if len(self) == 0:
      return 0.0
    total = sum(sequence.gc_content() for sequence in self.dna_sequences)
    return total / len(self)

if __name__ == "__main__":
  collection = SequenceCollection()
  collection.add_sequence(DNASequence("P001", "AGCTTTTCA"))
  collection.add_sequence(DNASequence("P002", "GCGCGCGC"))
  print(len(collection))
  print(collection.get_by_id("P001"))
  print(collection.average_gc_content())
