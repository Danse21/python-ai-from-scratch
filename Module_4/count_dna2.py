
from collections import Counter
def count_nucleotide(dna: str) -> tuple[int, int, int, int]:
  """Count A, C, G, T occurances in a DNA string. Returns counts in that order."""
  counts = Counter(dna)
  return counts['A'], counts['C'], counts['G'], counts['T']
if __name__ == "__main__":  # means: only run this block of code if this file was executed directly
  dna_nucleotide = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"
  a, c, g, t = count_nucleotide(dna_nucleotide)
  print(f"{a} {c} {g} {t}")
