# Build a pipeline function fasta_to_database(fasta_file: str, organism: str, conn)
# that: parses a FASTA file → validates each sequence (skips invalid ones with a warning instead of crashing) →
# converts to DNASequence objects → saves to the database → returns a summary dict with keys inserted, skipped, and total.
# Test it with a FASTA file that contains at least one invalid sequence.

# Describe the problem in plain English: Write a function that handles a fasta file, validates sequence, store the sequence in database and show operation summary
# What do I need to do? write an independent function and test that the function works as expected
# What's the primitive operation? parse a fasta file, validate each sequence, convert each record to DNASequence, save to database, show summary
# What Python tool does exactly that?

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
from config import DB_PATH
from Module_4_8_OOP.dna_sequence import DNASequence
from Module_5_2_SQL_Database.sql_in_function import save_sequence

def fasta_to_database(fasta_file: str, organism: str, conn):
  inserted = 0
  skipped = 0
  for record in  SeqIO.parse(fasta_file, "fasta"):         # Parse a FASTA file
    try:
      seq = DNASequence(record.id, str(record.seq))        # Validate and convert record to DNASequence object using DNASequence class methods
      organism = record.description.split(" ", 1)[1] if " " in record.description else organism
      save_sequence(seq, organism, conn)                   # Save to Database
      inserted += 1
    except ValueError as err:
      print(f"Warning: skipping {record.id} - {err}")
      skipped += 1
  return {"inserted": inserted, "skipped": skipped, "total": inserted + skipped}   # return a summary dict

if __name__ == "__main__":
  conn = sqlite3.connect(DB_PATH)
  # create a test fasta file
  test_records = [
    SeqRecord(Seq("AGTTCGCGATGAAGCTGCA"), id="T001", description="E. coli 16S rRNA"),
    SeqRecord(Seq("ATGXTAGCTAGXCTAACGT"), id="T002", description="E. coli lacZ"),
    SeqRecord(Seq("GCGCGCGCTTAAGGCCACCT"), id="T003", description="H. sapiens BRCA1"),
    SeqRecord(Seq("TTAXXGGATCCGGTACGATC"), id="T004", description="S. cerevisiae GAL4")
  ]
  with open("test_sequence.fasta", "w") as f:
    SeqIO.write(test_records, f, "fasta")

  result = fasta_to_database("test_sequence.fasta", "mixed", conn)    # "mixed" is a placeholder for the organism parameter
  print(result)
  conn.close()
