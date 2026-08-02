# Uses labeled test set: questions where with known chucks with the correct answer, to measure retrieval correctness.

from rag_embedding_vector_search import model, collection

eval_set = [
    {"query": "What database is used to store protein metadata?", "expected_keyword": "biodata.db"},
    # {"query": "Where does the app keep track of proteins between requests?", "expected_keyword": "biodata.db"}, # a bit tougher paraphrase question
    {"query": "How do you run the API with Docker?", "expected_keyword": "docker run"},
    {"query": "What model is used to generate protein embeddings?", "expected_keyword": "ESM-2"},
    {"query": "What happens before the Docker image gets built in CI?", "expected_keyword": "pytest"},
    {"query": "What amino acids does the API accept?", "expected_keyword": "20 standard"},
]

def evaluation_retrieval(eval_set, k=3):
  hits = 0
  reciprocal_ranks = []

  for item in eval_set:
    query_embeddings = model.encode([item["query"]]).tolist()
    results = collection.query(query_embeddings=query_embeddings, n_results=k)
    retrieved_docs = results["documents"][0]

    rank = None
    for i, doc in enumerate(retrieved_docs):
      if item["expected_keyword"] in doc:
        rank = i + 1 # store 1-indexed rank
        break

    if rank:
      hits += 1
      reciprocal_ranks.append(1 / rank)
    else:
      reciprocal_ranks.append(0)

  recall_at_k = hits / len(eval_set)
  mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
  return recall_at_k, mrr

recall, mrr = evaluation_retrieval(eval_set, k=3)
print(f"Recall@3: {recall:.2f}")
print(f"MRR: {mrr:.2f}")

"""
Reflection:
Recall@3 answers "for what fraction of my test questions did the correct chunk show up anywhere in the top 3" - a blunt pass/fail.
MRR (Mean Reciprocal Rank) is more forgiving of position: a correct answer ranked 1st scores 1.0, ranked 2nd scores 0.5,
ranked 3rd scored 0.33, and if it's missing entirely it scores 0. MRR shows exactly which position the answer is ranked.
Question: For any query that scored 0 (correct chunk never appeared in top 3), what's your hypothesis for why —
wording mismatch between the query and the chunk, chunk boundary problem, or something else?
Answer: I think the reason for any query that scored 0 will be due to wording mismatch between the query and the chunk. This reflects
back to previous answer of "slightly different query phrasing" as a way to improve vector distance.
"""
