# Code to test ValueError for invalid input (base character) scenarios

from collections import Counter
import io

def count_nucleotides(dna: str) -> tuple[int, int, int, int]:
  """Counts A, C, G, T occurrences in a DNA string.
    Raises:
    TypeError when input is not a string (e.g., numbers, files, lists)
    ValueError when input contains invalid character(s) in the DNA string.
  """
  # Type validation
  if not isinstance(dna, str):
    raise TypeError(f"Expected a string, but received {type(dna).__name__}")

  # Count DNA
  counts = Counter(dna)

  # Value Validation
  if not counts.keys() <= {"A", "C", "G", "T"}:
    invalid_bases = counts.keys() - {"A", "C", "G", "T"}
    raise ValueError(f"Invalid character(s) found in DNA string: {invalid_bases}")
  return counts['A'], counts['C'], counts['G'], counts['T']



