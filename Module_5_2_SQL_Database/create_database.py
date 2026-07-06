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
# print(df)

# Övning 2: Write three separate queries:
# All sequences from a specific organism
df2 = pd.read_sql_query("SELECT * FROM sequences WHERE organism = ?", conn, params=("H. sapiens",))
# print(df2)
# All sequences with gc_content above 50%, ordered highest to lowest
df3 = pd.read_sql_query("SELECT * FROM sequences WHERE gc_content > 50 ORDER BY gc_content DESC", conn)
# print(df3)
# The average gc_content across all sequences
df4 = pd.read_sql_query("SELECT AVG(gc_content) AS avg_gc_content FROM sequences", conn)
# print(df4)


# Övning 3:
# Create a second table organisms (columns: id, name, kingdom, genome_size).
# Insert matching organism data. Write a JOIN query that returns sample_id,
# gc_content, kingdom, and genome_size for all sequences. Then write a LEFT JOIN version
# and explain the difference in output.

cursor.execute("DROP TABLE IF EXISTS organisms")
cursor.execute("""
      CREATE TABLE IF NOT EXISTS organisms (
              id            INTEGER PRIMARY KEY AUTOINCREMENT,
              name          TEXT NOT NULL,
              kingdom       TEXT NOT NULL,
              genome_size   INTEGER NOT NULL
      )
""")
conn.commit()

data_organism = [
  ("E. coli", "Bacteria", 4600000),
  ("S. cerevisiae", "Fungi", 12100000),
  ("A. thaliana", "Plantae", 135000000),
  ("D. melanogaster", "Animalia", 143700000),
  ("H. sapiens", "Animalia", 3200000000)
]

# Insert the data above into the organisms table
cursor.executemany("""
      INSERT INTO organisms (name, kingdom, genome_size)
      VALUES (?, ?, ?)
""", data_organism)
conn.commit()

# Write (INNER) JOIN query that returns sample_id, gc_content, kingdom, and genome_size for all sequences
df5 = pd.read_sql_query("""
                        SELECT s.sample_id, s.gc_content, o.kingdom, o.genome_size
                        FROM sequences s
                        JOIN organisms o ON s.organism = o.name
                        """, conn)
print(df5)

# write a LEFT JOIN version and explain the difference in output.
df6 = pd.read_sql_query("""
                        SELECT s.sample_id, o.genome_size
                        FROM sequences s
                        LEFT JOIN organisms o ON s.organism = o.name
""", conn)
print(df6)

# The difference (INNER) JOIN query and LEFT JOIN query is that the JOIN query returns only the rows from both
# tables that have matches (value under sequences.organism == value under organisms.name)
# wheres the LEFT JOIN query returns all the rows from the left table and only rows in the right table
# that match the left table rows, with NaN for rows on the right table without matches.
# The choice between JOIN and LEFT JOIN is a deliberate decision: do you want to silently lose unmatched rows,
# or keep them and flag the gaps with NaN?

