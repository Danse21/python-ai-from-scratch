#
from fastapi import FastAPI, HTTPException
import sqlite3, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

app = FastAPI(title="Protein Function API", version="1.0.0")

@app.get("/")
def root():
  return {"message": "protein Function Prediction API", "status": "running"}

# Path parameter: the uniprot_id parameter is part of the URL (path)
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

# Query parameter: parameter passed as ?limited=10 in the URL
@app.get("/proteins")
def list_proteins(limit: int = 10):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("SELECT uniprot_id, protein_name FROM drug_targets LIMIT ?", (limit,))
  rows = cursor.fetchall()
  conn.close()
  return {"proteins": [{"uniprot_id": r[0], "protein_name": r[1]} for r in rows]}


"""
Q1. What is the difference between a path parameter (/protein/{uniprot_id}) and a query parameter (?limit=10)? When would you use each?
Answer: Path parameter is a mandatory path of URL. it is used to guide the HTTP request. On the other hand, query parameter can be omitted, mainly used as a filter.
Q2. What happens when you request P99999 and why is HTTPException(status_code=404) the correct response?
Answer: With P99999, it gives code: 404, Response body {"detail": "P99999 not found in the database"}. HTTPException is the correct
response because it is widely understood by every HTTP client (browser, another API, a Streamlit frontend). Status codes communicate outcome: 200 = OK, 404 = Not Found,
400 = Bad Request, 500 = server Error.
"""
