
def calculate_gc_content(dna: str) -> float:

  # Validate data type
  if not isinstance(dna, str):
    raise TypeError(f"Invalid data type input: {type(dna).__name__}")

  # Validate input characters
  for base in dna:
    if base not in {"A", "C", "G", "T"}:
      raise ValueError(f"Invalid base(s) found in the input: {base}")

  # Validate that input is not empty string
  if len(dna) == 0:
    raise ValueError(f"Invalid input, empty string: {dna}")

  # Process data
  gc_count = dna.count('G') + dna.count('C')
  total_nucleotide = len(dna)
  gc_percentage = gc_count / total_nucleotide * 100
  return gc_percentage
if __name__ == "__main__":
  dna_nucleotide = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"
  result = calculate_gc_content(dna_nucleotide)
  print(result)



