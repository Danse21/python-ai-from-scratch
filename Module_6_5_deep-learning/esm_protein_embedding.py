"""
  Load ESM-2 (esm2_t6_8M_UR50D — the small fast version). Fetch 6 protein sequences from UniProt:
  3 kinases and 3 non-kinases. Generate ESM embeddings for each. Train a LogisticRegression
  classifier on the embeddings to distinguish kinases from non-kinases.
"""

import requests
import torch
import esm
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def fetch_protein_sequence(query: str, max_result: int = 10) -> list[dict]:
  url = "https://rest.uniprot.org/uniprotkb/search"
  params = {
    "query": query,
    "format": "json",
    "size": max_result,
    "fields": "sequence,protein_name"
  }
  response = requests.get(url, params=params)
  results = response.json().get("results", [])
  proteins = []
  for result in results:
    seq = result.get("sequence", {}).get("value", "")
    length = result.get("sequence", {}).get("length", 0)
    if seq and length > 50:
      proteins.append({"sequence": seq, "length": length})
  return proteins

# Fetch 3 kinases and 3 non-kinases (proteases)
print("Fetching kinase proteins...")
kinases = fetch_protein_sequence("kinase AND reviewed:true AND organism_id:9606", 3)
print(f"Got {len(kinases)} kinases")

print("Fetching protease proteins...")
proteases = fetch_protein_sequence("protease AND reviewed:true AND organism_id:9606", 3)
print(f"Got {len(proteases)} proteases")

fetched_proteins = kinases + proteases
labels = [1] * len(kinases) + [0] * len(proteases)

# Load ESM-2 model
model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
batch_converter = alphabet.get_batch_converter()
model.eval()

# ESM requires list of (label, sequence) tuples
data = [(f"protein_{i}", p["sequence"]) for i, p in enumerate(fetched_proteins)]
batch_labels, batch_strs, batch_tokens = batch_converter(data)

# Generate embeddings
with torch.no_grad():
  esm_output = model(batch_tokens, repr_layers=[6])

# Extract per-residue embeddings via mean pooling over residue positions
token_embeddings = esm_output["representations"][6]
print(f"Token embedding shape: {token_embeddings.shape}")

embeddings = []
for i, (_, seq) in enumerate(data):
  emb = token_embeddings[i, 1:len(seq)+1].mean(0)
  embeddings.append(emb.numpy())

X = np.array(embeddings)
y = np.array(labels)
print(f"Feature matrix: {X.shape}")

# Split and Classify dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
print(classification_report(y_test, clf.predict(X_test)))
