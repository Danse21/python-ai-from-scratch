# Övning 1:
# Create a FASTA file manually with at least 4 sequences (use realistic headers with organism names).
# Parse it with SeqIO.parse() and print each record's ID, length, and GC content using gc_fraction().

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

records = [
  SeqRecord(Seq("AGTTCGCGATGAAGCTA"), id="P001", description="E. coli 16S rRNA"),
  SeqRecord(Seq("ATGCTAGCTAGGCTAACGT"), id="P002", description="E. coli lacZ"),
  SeqRecord(Seq("GCGCGCGCTTAAGGCCAT"), id="P003", description="H. sapiens BRCA1"),
  SeqRecord(Seq("TTACGGATCCGGTACGATC"), id="P004", description="S. cerevisiae GAL4")
]

# Create a fasta file
with open("sequence.fasta", "w") as f:
  SeqIO.write(records, f, "fasta")

# Parse the fasta file with SeqIO.parse()
for record in SeqIO.parse("sequence.fasta", "fasta"):
  gc = gc_fraction(record.seq) * 100
  print(f"ID: {record.id} | Length: {len(record.seq)} | GC {gc: .2f} %")
