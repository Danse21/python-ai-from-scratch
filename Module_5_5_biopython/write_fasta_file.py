# Write a FASTA file programmatically using SeqIO.write() — create 3 SeqRecord objects with
# realistic biological data and write them to a new .fasta file. Then immediately parse it back
# and verify the data is identical.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO

record_seq = [
    SeqRecord(Seq("ATGCGTATCGA"), id="V001", description="Test sequence 1"),
    SeqRecord(Seq("GCTAGCTAGCT"), id="V002", description="Test sequence 2"),
    SeqRecord(Seq("TTACGGCATGC"), id="V003", description="Test sequence 3"),
]

# Create a fasta file
with open("verified.fasta", "w") as f:
  SeqIO.write(record_seq, f, "fasta")

# Parse the fasta file and convert records to list
parsed_records = list(SeqIO.parse("verified.fasta", "fasta"))

# Verify data: for each parsed record, find its matching original and compare ID and sequence.
# zip() pairs parsed with original
for parsed, original in zip(parsed_records, record_seq):
  if parsed.id == original.id:
    print(f"Confirmed ID matched: {parsed.id}")
  else:
    print(f"ID mismatch: got {parsed.id}, expected {original.id}")
  if parsed.seq == original.seq:
    print(f"Confirmed sequence matched: {parsed.seq}")
  else:
    print(f"Sequence mismatch: got {parsed.seq}, expected {original.seq}")
