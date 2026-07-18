# Write a function fetch_protein_data(uniprot_id: str) -> dict that fetches sequence, organism,
# protein name, and gene name from UniProt REST API. Test it on at least 3 proteins relevant to
# drug discovery: BRCA1 (P38398), TP53 (P04637), and EGFR (P00533). Store results in a
# pandas DataFrame and save to your SQLite database.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import pandas as pd
from config import DB_PATH
import sqlite3

def fetch_protein_data(uniprot_id: str) -> dict:
  """Fetches key protein data from Uniprot for a single ID"""
  url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
  params = {"format": "json"}
  response = requests.get(url, params=params)
  if response.status_code != 200:
    print(f"Failed to fetch {uniprot_id}: HTTP {response.status_code}")
    return {}

  protein_data = response.json()
  sequence = protein_data.get("sequence", {}).get("value", "")
  organism = protein_data.get("organism", {}).get("scientificName", "")
  protein_name = protein_data.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "")
  genes = protein_data.get("genes", [])
  gene_name = genes[0].get("geneName", {}).get("value", "") if genes else ""

  return {
    "uniprot_id": uniprot_id,
    "protein_name": protein_name,
    "gene_name": gene_name,
    "organism": organism,
    "sequence": sequence
  }

def save_to_database(records: list[dict]):
  """store result in pandas DataFrame and save in SQlite database"""
  df = pd.DataFrame(records)
  conn = sqlite3.connect(DB_PATH)
  df.to_sql("drug_targets", conn, if_exists="replace", index=False)
  """terminate database connection"""
  conn.close()
  print(f"Saved {len(df)} proteins to database.")

if __name__ == "__main__":
  target_proteins = ["P38398","P04637", "P00533"]
  protein_records = []
  for protein_id in target_proteins:
    data = fetch_protein_data(protein_id)
    if data:
      """Only append if data fetched successfully"""
      protein_records.append(data)
    if protein_records:
      df = pd.DataFrame(protein_records)
  print(df[["uniprot_id", "protein_name", "gene_name", "organism"]])
  save_to_database(protein_records)

