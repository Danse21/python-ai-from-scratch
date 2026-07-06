# Övning 4
# Connect your OOP work to SQL: write a function save_sequence(seq: DNASequence, organism: str, conn)
# that takes a DNASequence object and inserts it into the database, computing gc_content automatically.
# Write a second function load_sequences(conn) -> list[DNASequence] that reads all rows and
# returns a list of DNASequence objects. Test both.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
from Module_4_8_OOP.dna_sequence import DNASequence

def save_sequence(seq: DNASequence, organism: str, conn) -> None:
  cursor = conn.cursor()
  cursor.execute("""
        INSERT OR IGNORE INTO sequences (sample_id, sequence, gc_content, organism)
        VALUES (?, ?, ?, ?)
  """, (seq.sample_id, seq.sequence, seq.gc_content(), organism))
  conn.commit()

# Query all rows from sequences table and return a list of DNA Sequence objects
def load_sequences(conn) -> list[DNASequence]:
  cursor = conn.cursor()
  cursor.execute("SELECT sample_id, sequence FROM sequences")
  rows = cursor.fetchall()
  result = []
  for row in rows:
    result.append(DNASequence(row[0], row[1]))
  return result

# Test both functions
if __name__ == "__main__":
  conn = sqlite3.connect("biodata.db")
  new_seq = DNASequence("P006", "AGTTCGCGATGAAGCTA")
  save_sequence(new_seq, "A. thaliana", conn)
  sequences = load_sequences(conn)
  for s in sequences:
    print(s)
  conn.close()

