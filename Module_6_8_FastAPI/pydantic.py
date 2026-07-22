"""
GET request fetch data from the server
POST request send data to the server
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

app = FastAPI(title="Protein Function API", version="1.0.0")

# Pydantic model: defines exactly what JSON the client must send
class SequenceRequest(BaseModel):
  uniprot_id: str
  sequence: str
  organism: str = "Unknown"   # optional field with default

class SequenceResponse(BaseModel):
  uniprot_id: str
  sequence_length: int
  gc_content: float | None = None
  message: str

@app.get("/protein/{uniprot_id}")
def get_protein(uniprot_id: str):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM drug_targets WHERE uniprot_id = ?", (uniprot_id,))
  row = cursor.fetchone()
  conn.close()
  if row is None:
    raise HTTPException(status_code=404, detail=f"{uniprot_id} not found in the database")
  return {"uniprot_id": row[0], "protein_name": row[1], "gene_name": row[2], "organism": row[3]}

@app.post("/protein", response_model=SequenceResponse)
def submit_protein(request: SequenceRequest):
  # Validate sequence, only 20 standard amino acids
  valid_aa = set("ACDEFGHIKLMNPQRSTVWY")
  invalid = [aa for aa in request.sequence.upper() if aa not in valid_aa]
  if invalid:
    raise HTTPException(status_code=400, detail=f"Invalid amino acids: {set(invalid)}")

  # Save to database
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("""
            INSERT OR IGNORE INTO drug_targets (uniprot_id, protein_name, gene_name, organism)
            VALUES (?, ?, ?, ?)
  """, (request.uniprot_id, "Submitted manually", "", request.organism))
  conn.commit()
  conn.close()

  return SequenceResponse(
    uniprot_id=request.uniprot_id,
    sequence_length=len(request.sequence),
    message=f"Protein {request.uniprot_id} saved successfully"
  )


"""
Reflection questions:
Q1: What does response_model=SequenceResponse do and why is it useful?
Answer: response_model=SequenceResponse is used by FastAPI to automatically validate and filter response so
that only the decleared fields reach the client (browser or a Streamlit frontend). Also, it generates the
response schema in /docs so API consumers know exactly what JSON structure to expect back., without it callers
don't know what they will receive until they call it.

Q2: What HTTP status code is returned for the invalid sequence, and what does that code mean?
Answer: status code returned is 400, which means Bad Request, ie., invalid input.

Q3: What is Pydantic doing in this code that you would otherwise have to write manually?
Answer: What Pydantic is doing is pre-defining data type that is expected to be received or sent, which can
be reused and not manually defined whenever it's needed.
"""
