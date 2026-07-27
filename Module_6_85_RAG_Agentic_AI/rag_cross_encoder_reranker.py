# A cross-encoder reranker looks at the query and a candidate chunk together, in a single forward pass,
# instead of comparing two independently-computed embeddings. Because is slower compared to vector search,
# but more precise (and one cannot precompute chunk vectors in advance to improve speed), production RAG
# runs it only on the vector search's top-k, as a second, more expensive filtering pass.

from sentence_transformers import CrossEncoder
from rag_embedding_vector_search import collection, model

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, candidates: list[str], top_k: int = 3):
  pairs = [(query, c) for c in candidates]
  scores = reranker.predict(pairs)
  ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
  return ranked[:top_k]

# Reuse the vector search results as candidates
db_results = collection.query(query_embeddings=model.encode(["What database is used to store protein metadata?"]).tolist(), n_results=5)
hamster_results = collection.query(query_embeddings=model.encode(["how does the classifier handle Chinese hamster ovary cell proteins?"]).tolist(), n_results=5)

if __name__ == "__main__":
  print("Reranked: database question")
  for doc, score in rerank("What database is used to store protein metadata?", db_results["documents"][0]):
    print(f"Score: {score:.4f} | {doc[:100]}")

  print("\nReranked: hamster question")
  for doc, score in rerank("how does the classifier handle Chinese handle hamster ovary cell proteins?", hamster_results["documents"][0]):
    print((f"Score: {score:.4f} | {doc[:100]}"))

"""
Reflection:
Q1. Cross-encoder scores are raw logits, not bounded distances — negative scores generally mean "not relevant,"
positive means "relevant," and the magnitude matters. Does the hamster question's top reranked score look clearly
negative/low compared to the database question's?
Answer: Yes, the hamster question's top reranked score = -11.02 is clearly negative/low compare to that of database
question's +5.22, that is a 16-point difference. The ability of production RAG systems to rerank before generation
underscores the relevance of the cross-encoder.
Q2. Given what you see, would a fixed rule like "if top reranker score < 0, respond with 'I don't have information
about that' instead of calling the LLM" be a reasonable production safeguard here? Why or why not?
Answer: Yes, the fix would be a reasonable safeguard here, and 0 is a sensible natural cutoff (threshold) for this
particular reranker. It is important to note here that different reranker models will have its own threshold, therefore,
checking or validating a threshold against a labeled set of "relevant" or "not relevant" query-chunk pairs is needed
(see retrieval evealuation).
"""
