# Embedding & vector search: This is a phenomenon in which a chunk of text becomes searchable by converting it into
# a vector of numbers, an embedding, where semantically similar text produces mathematically close vectors.
# close = cosine similar or its inverse, distance.

from sentence_transformers import SentenceTransformer
import chromadb
from rag_chunking_strategies import chunk_recursive

model = SentenceTransformer("all-MiniLM-L6-v2")   # small fast model with good baseline

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("project_docs")

with open("README.md") as f:
  readme = f.read()

chunks = chunk_recursive(readme)
embeddings = model.encode(chunks).tolist()

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)
# query = "What database is used to store protein metadata?"
query = "how does the classifier handle Chinese hamster ovary cell proteins?"
query_embedding = model.encode([query]).tolist()

results = collection.query(query_embeddings=query_embedding, n_results=3)

if __name__ == "__main__":
  for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"Distance: {distance:.4f}")
    print(doc[:200])
    print("---")

"""
Reflection question:
Q1. For the encoding question, does the top-ranked chunk (lowest distance) actually contain the SQLite/`biodata.db` line from Architecture section?
If not immediately, what would you adjust — chunk size, overlap, or something else?
Answer: Yes, the top-ranked chunk (lowest distance) contains the database information. Output: Distance: 0.8408, SQLite database (`biodata.db`).
One can also adjust by getting a corpus (text) with more borderline-similar content or a slightly different query phrasing.
Q2. Vector search always returns your n_results top matches, even for the Chinese hamster query where nothing in the corpus is actually relevant.
What did it return, and why is that a real production problem if you don't handle it downstream?
Answer: It returns "the least unrelated things I have" on the README.md file. This is regardless of whether the gap happens to be wide or narrow,
which is the real production problem: a raw distance value has no inherent meaning on its own.
Q3. all-MiniLM-L6-v2 is an English-optimized model. Stena Fastigheter's real documents (leases, maintenance logs) would very likely be in Swedish.
What would you expect to go wrong if you embedded Swedish text with this model, and what's the fix (look up paraphrase-multilingual-MiniLM-L12-v2 if you're unsure)?
Answer: I would expect the vector search performance to perform significantly bad. And the embedded Swedish text with this model will face tokenizer fragmentation,
semantic misalignment and poor retrieval, and cross-lingual failure. A fix is to switch to 'paraphrase-multilingual-MiniLM-L12-v2' model that supports over 50 languages
align vector space through knowledge distillation, and enable cross-lingual search.
"""
