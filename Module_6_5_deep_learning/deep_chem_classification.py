"""Load the BBBP dataset, train a GraphConvModel, evaluate on train and test sets using ROC-AUC.
Then load a second dataset — BACE (β-secretase inhibition — Alzheimer's drug discovery) using
dc.molnet.load_bace_classification(). Compare AUC scores between the two datasets.
"""
import requests, io
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import RDLogger
RDLogger.DisableLog("rdApp.*")

# Task
# BBBP = Blood-Brain Barrier Penetration
# Predict whether a drug molecule can cross the blood-brain barrier
# Input: SMILES strings (molecular structure as text)
# Output: 1 = penetrates, 0 = does not penetrate

# Download BBBP dataset
print("Downloading BBBP dataset...")
url = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv"
df = pd.read_csv(url)
print(f"Loaded {len(df)} molecules")
print(df[['name', 'p_np', 'smiles']])

# Compute Morgan fingerprints (ECFP4) with RDKit
def smiles_to_fingerprint(smiles: str, radius: int = 2, n_bits: int = 1024):
  mol = Chem.MolFromSmiles(smiles)
  if mol is None:
    return None
  fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
  return np.array(fp, dtype=np.float32)

X, y = [], []
skipped = 0
for _, row in df.iterrows():
  fp = smiles_to_fingerprint(str(row["smiles"]))
  if fp is not None:
    X.append(fp)
    y.append(float(row["p_np"]))
  else:
    skipped += 1

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32).reshape(-1, 1)
print(f"\nFeaturized: {len(X)} molecules ({skipped} skipped as invalid SMILES)")

# Split and convert to tensors
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Extract numpy arrays and convert to tensors
X_train_t = torch.FloatTensor(X_train)
y_train_t = torch.FloatTensor(y_train)
X_test_t = torch.FloatTensor(X_test)
y_test_t = torch.FloatTensor(y_test)

# # Build PyTorch model
class MoleculeClassifier(nn.Module):
  def __init__(self):
    super().__init__()
    self.network = nn.Sequential(
      nn.Linear(1024, 256), nn.ReLU(), nn.Dropout(0.2),
      nn.Linear(256, 128), nn.ReLU(), nn.Dropout(0.2),
      nn.Linear(128, 1), nn.Sigmoid()
    )
  def forward(self, x):
    return self.network(x)

model = MoleculeClassifier()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
print("\nTraining...")
for epoch in range(1, 51):
  model.train()
  optimizer.zero_grad()
  pred = model(X_train_t)
  loss = criterion(pred, y_train_t)
  loss.backward()
  optimizer.step()

  if epoch % 10 == 0:
    model.eval()
    with torch.no_grad():
      val_pred = model(X_test_t)
      val_loss = criterion(val_pred, y_test_t)
      auc = roc_auc_score(y_test_t.numpy(), val_pred.numpy())
    print(f"Epoch {epoch:2d}: Train Loss={loss.item():.4f}, Validation Loss={val_loss.item():.4f}, ROC-AUC={auc:.4f}")

# Predict on new molecules
print("\n Predicting new molecules...")
new_smiles = [
    ("Aspirin",       "CC(=O)Oc1ccccc1C(=O)O"),       # pain reliever
    ("Caffeine",      "Cn1cnc2c1c(=O)n(c(=O)n2C)C"),  # stimulant (CNS active)
    ("Ibuprofen",     "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),  # anti-inflammatory
    ("Dopamine",      "NCCc1ccc(O)c(O)c1"),           # neurotransmitter
]
model.eval()
with torch.no_grad():
  for name, smiles in new_smiles:
    fp = smiles_to_fingerprint(smiles)
    x = torch.FloatTensor(fp).unsqueeze(0)
    probability = model(x).item()
    label = "YES" if probability > 0.5 else "NO"
    print(f"{name:12s}: BBB peneration = {label} (confidence: {probability:.3f})")


# Reflection questions
"""
Question 1:
  The training curves show ROC-AUC peaked at epoch 20–30 then slightly declined,
  while train loss continued falling. What technique would you use to automatically
  stop training at the best point — and why does this matter for a drug discovery
  model in practice?
  Answer:
  Early stopping: By monitoring validation loss at each epoch and saving the model weights
  whenever it improves. When validation loss stops improving for N consecutive epochs
  (called patience), you stop training and restore the best weights.
  In drug discovery, a falsely confident model that predicts a wrong molecule crosses the
  BBB could send a drug into clinical trials that fails, costing years and hundreds of
  millions of dollars.

Question 2:
  Dopamine predicted BBB = NO (confidence 0.136). Dopamine is a neurotransmitter that
  acts in the brain — so is the model wrong? Research what drug is actually given to
  Parkinson's patients who need more brain dopamine, and explain why that molecule is
  used instead of dopamine itself.
  Answer:
  The model rightly predicted that dopamine does not penetrate blood-brain barrier (BBB).
  Parkinson's patients are usually treated with Levodopa, a direct metabolic precursor to
  dopamine. Levodopa is a single amino acid and is a substrate for the brain's
  LAT1 amino acid transporter, which actively carries it across the blood-brain barrier.

Question3:
  Caffeine returned confidence 1.000 — absolute certainty. What does a confidence of
  exactly 1.000 tell you about the model's calibration, and should you trust it more or less
  than a confidence of 0.85?
  Answer:
  This is due to sigmoid saturation. When the network's final linear layer produces a
  very large positive number, the model overfits and becomes extremely confident, thus
  pushes outputs toward 0 or 1 rather than staying in the middle range.
  I would trust the result less than a confidence of 0.85. A well-calibrated
  model in drug discovery should express uncertainty, not absolute certainty.
  confidence of 1.000 is a sign the model is overconfident, not that it's more accurate.
"""



# Build a deep learning model (Extended Connectivity Fingerprint, ECFP) that Classifies drug molecule dataset
