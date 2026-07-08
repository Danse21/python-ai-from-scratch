# Övning 1:
# Create a FASTA file manually with at least 4 sequences (use realistic headers with organism names).
# Parse it with SeqIO.parse() and print each record's ID, length, and GC content using gc_fraction().

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
from Module_4_8_OOP.dna_sequence import DNASequence
from Module_5_2_SQL_Database.sql_in_function import save_sequence

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
  #print(f"ID: {record.id} | Length: {len(record.seq)} | GC {gc: .2f} %")

# Övning 2
# Parse the same FASTA file and convert each record into a DNASequence object from your Modul 4.8 class.
# Print each object using __str__. Then save all sequences to biodata.db using your save_sequence() function from Modul 5.2.

from config import DB_PATH
import sqlite3

conn = sqlite3.connect(DB_PATH)

for record in SeqIO.parse("sequence.fasta", "fasta"):
  seq = DNASequence(record.id, str(record.seq))
  print(seq)
organism = record.description.split(" ", 1)[1]    # Removes first part of description and leaves the second part.
save_sequence(seq, organism, conn)

