"""Build a function protein_function_pipeline(proteins: list[dict], labels: list[int], conn)
that: fetches sequences from UniProt → generates ESM embeddings → trains a classifier →
evaluates → saves results to your SQLite database → returns a summary dict."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
import esm
import requests
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from config import DB_PATH



def fetch_proteins_by_query(query: str, max_result: int = 100) -> list[dict]:
  """Fetch from Uniprot by query, return id and sequence"""
  url = f"https://rest.uniprot.org/uniprotkb/search"
  params = {
    "query": query,
    "format": "json",
    "size": max_result,
    "fields": "accession,sequence"
    }
  response = requests.get(url, params=params)
  results = response.json().get("results", [])
  proteins = []
  for result in results:
    uid = result.get("primaryAccession", "")    # uniprot_id
    seq = result.get("sequence", {}).get("value", "")
    length = result.get("sequence", {}).get("length", 0)
    if seq and length > 50:
      proteins.append({"uniprot_id": uid, "sequence": seq})
  return proteins

def protein_function_pipeline(proteins: list[dict], labels: list[int], conn):
  """
  Full pipeline:
  - Fetch sequences from Uniprot
  - Generate ESM-2 embeddings
  - save to SQLite
  - Train LogisticRegression on embeddings
  - Report classification results
  """
  # Fetch sequences
  valid_proteins = []
  valid_labels = []
  for protein, label in zip(proteins, labels):   # pairs labels with proteins
    if protein:
      valid_proteins.append(protein)
      valid_labels.append(label)
  print(f"Fetched {len(valid_proteins)} proteins")

  # Generate ESM-2 embeddings
  esm_model, alphabet = esm.pretrained.esm2_t12_35M_UR50D()
  batch_converter = alphabet.get_batch_converter()
  esm_model.eval()

  data_esm = [(p["uniprot_id"], p["sequence"]) for p in valid_proteins]
  _, _, batch_tokens = batch_converter(data_esm)

  with torch.no_grad():
    results = esm_model(batch_tokens, repr_layers=[12])

  token_embeddings = results["representations"][12]
  embeddings = []
  for i, (_, seq) in enumerate(data_esm):
    emb = token_embeddings[i, 1:len(seq)+1].mean(0).numpy()
    embeddings.append(emb)

  X = np.array(embeddings)
  y = np.array(valid_labels)
  print(f"Embedding matrix: {X.shape}")

  # Save to SQLite
  df = pd.DataFrame([{
    "uniprot_id": p["uniprot_id"],
    "sequence": p["sequence"],
    "label": lbl
  } for p, lbl in zip(proteins, valid_labels)])
  df.to_sql("protein_embeddings", conn, if_exists="replace", index=False)
  print(f"Saved {len(df)} proteins to database")

  # Train LogisticRegression on embeddings
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
  clf = LogisticRegression(max_iter=1000)
  clf.fit(X_train, y_train)

  # Evaluate: Report classification results
  print("\nClassification Report...")
  print(classification_report(y_test, clf.predict(X_test)))
  return clf

if __name__ == "__main__":
  # Fetch many proteins by query instead of hardcoding IDs
  kinases = fetch_proteins_by_query("kinase AND reviewed:true AND organism_id:9606", max_result=30)
  proteases = fetch_proteins_by_query("protease AND reviewed:true AND organism_id:9606", max_result=30)
  print(f"Fetched {len(kinases)} kinases, {len(proteases)} proteases")
  all_proteins = kinases + proteases
  labels = [1] * len(kinases) + [0] * len(proteases)
  conn = sqlite3.connect(DB_PATH)
  clf = protein_function_pipeline(all_proteins, labels, conn)
  conn.close()


