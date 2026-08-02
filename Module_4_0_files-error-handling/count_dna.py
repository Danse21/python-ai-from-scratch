# Given a DNA string
# Count the number of times that the symbols 'A', 'C', 'G', and 'T' occur in the string
from collections import Counter
dna_nucleotide = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"
count_dna = Counter(dna_nucleotide)
ordered_count = [count_dna['A'], count_dna['C'], count_dna['G'], count_dna['T'] ]
output = ' '.join(map(str, ordered_count))
print(output)