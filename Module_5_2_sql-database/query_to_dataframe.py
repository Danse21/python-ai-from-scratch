# Övning 5
# Write a function query_to_dataframe(query: str, conn) -> pd.DataFrame that executes any SQL query and
# returns the result as a Pandas DataFrame. Use it to run two different queries and display the results.
# Then add a GROUP BY query that shows sequence count and average GC content per organism.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH
import sqlite3
import pandas as pd

def query_to_dataframe(query: str, conn) -> pd.DataFrame:
  return pd.read_sql_query(query, conn)

if __name__ == "__main__":
  conn = sqlite3.connect(DB_PATH)
  q1 = query_to_dataframe("SELECT * FROM sequences", conn)
  q2 = query_to_dataframe("""
                        SELECT s.sample_id, o.genome_size
                        FROM sequences s
                        LEFT JOIN organisms o ON s.organism = o.name
                          """, conn)
  q3 = query_to_dataframe("""SELECT organism, COUNT(*) as sequence_count, AVG(gc_content) as avg_gc
                          FROM sequences
                          GROUP BY organism
                          """, conn)
  print(q1)
  print(q2)
  print(q3)
