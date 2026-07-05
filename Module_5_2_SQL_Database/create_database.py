# Create a biodata.db database with a sequences table
# (columns: id, sample_id, sequence, gc_content, organism).
# Insert at least 5 rows with realistic data. Then query and print all rows.

import sqlite3
import pandas as pd

# Create the .db file
# SQLite (SQL without a server) stores an entire database in a single .db file
conn = sqlite3.connect("biodata.db")   # Connects to the database
cursor = conn.cursor()   # used to execute SQL commands

# Create a sequence table
cursor.execute("DROP TABLE IF EXISTS sequences")
cursor.execute("""
  CREATE TABLE IF NOT EXISTS sequences (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id   TEXT NOT NULL UNIQUE,
        sequence    TEXT NOT NULL,
        gc_content  FLOAT,
        organism    TEXT
  )
""")
conn.commit()     # save the changes

data = [
  ("P001", "AGCTTTTCA", 33.33, "E. coli"),
  ("P002", "GCGCGCGC", 100.0, "H. sapiens"),
  ("P003", "ATATATATAT", 0.0, "S. cerevisiae"),
  ("P004", "AGCTAGCT", 50.0, "M. musculus"),
  ("P005", "AGCTAGCCTG", 60.0, "O. sativa")
]

# Insert data into the sequences table
cursor.executemany("""
    INSERT INTO sequences (sample_id, sequence, gc_content, organism)
    VALUES (?, ?, ?, ?)
""", data)
conn.commit()

# Query and print all rows
df = pd.read_sql_query("SELECT * FROM sequences", conn)
print(df)

# Write three separate queries:
# All sequences from a specific organism
df2 = pd.read_sql_query("SELECT * FROM sequences WHERE organism = ?", conn, params=("H. sapiens",))
print(df2)
# All sequences with gc_content above 50%, ordered highest to lowest
df3 = pd.read_sql_query("SELECT * FROM sequences WHERE gc_content > 50 ORDER BY gc_content DESC", conn)
print(df3)
# The average gc_content across all sequences
df4 = pd.read_sql_query("SELECT AVG(gc_content) AS avg_gc_content FROM sequences", conn)
print(df4)

