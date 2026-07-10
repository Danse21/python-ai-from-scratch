# Load your sequences table from biodata.db into a DataFrame using pd.read_sql_query().
# Add a new column length computed from the sequence strings. Filter rows where GC content is
# above the mean. Group by organism and compute mean GC content and mean length per organism.

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH
import sqlite3
import pandas as pd
import numpy as np


conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM sequences", conn)
df["length"] = df["sequence"].str.len()
reorder_column = ["id", "sample_id", "sequence", "length", "gc_content", "organism"]
df = df[reorder_column]
# Filter rows where GC content is above the mean
mean_gc = np.mean(df["gc_content"])   # 52.28
print(df[df["gc_content"] > mean_gc])

# Multiple aggregations: Group by organism and compute mean GC content and mean length per organism
grouped = df.groupby("organism").agg(
  avg_cg = ("gc_content", "mean"),
  mean_length = ("length", "mean")
)
print(grouped)

