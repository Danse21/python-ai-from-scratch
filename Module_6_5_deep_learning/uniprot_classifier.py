# Write a function fetch_protein_data(uniprot_id: str) -> dict that fetches sequence, organism,
# protein name, and gene name from UniProt REST API. Test it on at least 3 proteins relevant to
# drug discovery: BRCA1 (P38398), TP53 (P04637), and EGFR (P00533). Store results in a
# pandas DataFrame and save to your SQLite database.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from cancer_classifier_neural_network import CancerClassifier

# Fetch protein from Uniprot REST API
def fetch_unique_proteins(query: str, max_result: int = 100) -> list[dict]:
  url = "https://rest.uniprot.org/uniprotkb/search"
  params = {
    "query": query,
    "format": "json",
    "size": max_result,
    "fields": "accession,sequence,length,mass,protein_name"
  }
  response = requests.get(url, params=params)
  results = response.json().get("results", [])
  proteins = []
  for entry in results:
    seq = entry.get("sequence", {}).get("value", "")
    length = entry.get("sequence", {}).get("length", 0)
    mass = entry.get("sequence", {}).get("mass", 0)
    if seq and length > 50:
      proteins.append({"sequence": seq, "length": length, "mass": mass})
  return proteins

# Feature engineering from sequence
def extract_features(protein: dict) -> list[float]:
  seq = protein["sequence"]
  length = protein["length"]
  mass = protein["mass"]
  amino_acids = "ACDEFGHIKLMNPQRSTVWY"    # 20 amino acid composition
  composition = [seq.count(aa) / length for aa in amino_acids]

  # Physiochemical features
  charged = (seq.count("K") + seq.count("R") + seq.count("D") + seq.count("E")) / length
  hydrophobic = (seq.count("L") + seq.count("I") + seq.count("V") + seq.count("F")) / length
  return composition + [charged, hydrophobic, length / 1000, mass / 100000]

# Build dataset
# Fetch two classes: kinases (label=1) and proteases (label=0)
print("Fetching kinase proteins...")
kinases = fetch_unique_proteins("kinase AND reviewed:true AND organism_id:9606", 80)    # organism_id:9606: 9606 is the NCBI taxonomy ID for Homo sapiens
print(f"Got {len(kinases)} kinases")

print("Fetching protease proteins...")
proteases = fetch_unique_proteins("protease AND reviewed:true AND organism_id:9606", 80)
print(f"Got {len(proteases)} proteases")

X = []
y = []
for p in kinases:
  X.append(extract_features(p))
  y.append(1)
for p in proteases:
  X.append(extract_features(p))
  y.append(0)

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32).reshape(-1, 1)
print(f"\n Dataset: {X.shape[0]} proteins, {X.shape[1]} features each")

# Preprocess dataset and split
scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)    # Transform only, do not fit, otherwise test data leaked

# Convert to PyTorch tensor
X_train_t = torch.FloatTensor(X_train)
X_test_t = torch.FloatTensor(X_test)
y_train_t = torch.FloatTensor(y_train)
y_test_t = torch.FloatTensor(y_test)

# Reuse CancerClassifier architecture
input_size = X_train_t.shape[1]     # 24 features
model = CancerClassifier(input_size=input_size, hidden_size=64, output_size=1)
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

# Train model
epochs = 150
for epoch in range(epochs):
  model.train()
  optimizer.zero_grad()
  pred = model(X_train_t)
  loss = criterion(pred, y_train_t)
  loss.backward()
  optimizer.step()
  if (epoch + 1) % 30 == 0:
    model.eval()
    with torch.no_grad():
      val_pred = model(X_test_t)
      val_loss = criterion(val_pred, y_test_t)
      acc = ((val_pred > 0.5).float() == y_test_t).float().mean()
    print((f"Epoch {epoch+1}: Train Loss={loss.item():.4f}, Validation Loss={val_loss.item():.4f}, Accuracy={acc:.4f}"))

print("\n Done. Model trained on real Uniprot protein data.")

# The Accuracy at epoch 150 is 0.6562 (65.6%).
# Amino acid composition is a weak signal for distinguishing protein function. A kinase and a protease
# can have very similar amino acid frequencies. What differentiates them is their amino acid arrangement
# and 3D structure, and not just amino acids present.
# This draw back is provided for by protein language models (ESM, ProtBERT) which encodes contextual
# sequence information.
