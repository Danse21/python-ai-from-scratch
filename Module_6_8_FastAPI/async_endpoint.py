from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import torch, esm
import sqlite3, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH
from sklearn.linear_model import LogisticRegression
import pickle

# Pydantic models
class PredictRequest(BaseModel):
  sequence: str

class PredictResponse(BaseModel):
  sequence_length: int
  predicted_class: str
  confidence: float

# Load model and ESM at startup
ml_model = None
esm_model = None
alphabet = None

@asynccontextmanager
async def lifespan(app: FastAPI):
  """Runs once at startup, loads models into memory"""
  global ml_model, esm_model, alphabet
  print("Loading ESM-2 model...")
  esm_model, alphabet = esm.pretrained.esm2_t12_35M_UR50D()
  esm_model.eval()
  classifier_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classifier.pkl")
  if os.path.exists(classifier_path):
    with open(classifier_path, "rb") as f:
      ml_model = pickle.load(f)
      print("Classifier loaded.")
  else:
    print("Warning: no classifier.pkl found")
  yield     # server runs here
  print("Shutting down.")

app = FastAPI(title="Protein Function API", version="1.0.0", lifespan=lifespan)

# Define endpoints
@app.get("/")
async def root():
  return {"message": "Protein Function Prediction API", "status": "running"}

@app.get("/Protein/{uniprot_id}")
async def get_protein(uniprot_id: str):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM drug_targets WHERE uniprot_id = ?", (uniprot_id,))
  row = cursor.fetchone()
  conn.close()
  if row is None:
    raise HTTPException(status_code=404, detail=f"{uniprot_id} not found")
  return {"uniprot_id": row[0], "protein_name": row[1], "gene_name": row[2], "organism": row[3], "sequence": row[4]}

@app.post("/predict", response_model=PredictResponse)
async def predict_function(request: PredictRequest):
  if not request.sequence.strip():
    raise HTTPException(status_code=422, detail="Sequence cannot be empty")
  if ml_model is None:
    raise HTTPException(status_code=503, detail="Classifier not loaded.")

  # Generate ESM embedding
  batch_converter = alphabet.get_batch_converter()
  data = [("query", request.sequence)]
  _, _, tokens = batch_converter(data)

  with torch.no_grad():
    output = esm_model(tokens, repr_layers=[12])

  embedding = output["representations"][12][0, 1:len(request.sequence)+1].mean(0).numpy()
  X = embedding.reshape(1, -1)

  pred = ml_model.predict(X)[0]
  prob = ml_model.predict_proba(X)[0][pred]
  label = "kinase" if pred == 1 else "protease"

  return PredictResponse(
    sequence_length=len(request.sequence),
    predicted_class=label,
    confidence=round(float(prob), 3)
  )

"""
Reflection question:
What does async def do differently from regular def, and why does it matter when
multiple users call your API at the same time?
Answer: async allows the server to handle multiple requests concurrently without blocking.
With regular def, one slow request (like database query, file read, etc) blocks other requests
behind it. async def, on the other hand, pauses a slow request (or operation e.g., await database_query())
and immediately handles the next one. Later when the slow operation finishes, it resumes it again.
"""
