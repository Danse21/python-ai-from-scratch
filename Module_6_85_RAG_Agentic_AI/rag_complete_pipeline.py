# Uses actual LLM (Groq) to generate an answer

import os
from dotenv import load_dotenv
from groq import Groq
from rag_embedding_vector_search import model, collection
from rag_cross_encoder_reranker import rerank

os.environ["TOKENIZERS_PARALLELISM"] = "false"     # clears noisy warning
load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_answer(query: str, k: int = 5, rerank_threshold: float = 0.0) -> str:
  # Vector search (broad net)
  query_embedding = model.encode([query]).tolist()
  results = collection.query(query_embeddings=query_embedding, n_results=k)
  candidates = results["documents"][0]

  # Rerank (precise filter)
  ranked = rerank(query, candidates, top_k=3)

  # Threshold gate: give no answer if nothing is relevant (positive score)
  top_chunk, top_score = ranked[0]
  if top_score < rerank_threshold:
    return "I don't have information about that in this document."

  # Assemble context from chunks with positive scores
  context_chunks = [doc for doc, score in ranked if score >= rerank_threshold]
  context = "\n\n---\n\n".join(context_chunks)

  # Generate answer (grounded strickly in retrieved context)
  prompt = f"""
  Answer the question using ONLY the context below.
  If the context doesn't contain the answer, say so explicity rather than guessing.

  Context: {context}
  Question: {query}
  Answer:"""
  response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
  )
  return response.choices[0].message.content

print(generate_answer("What database is used to store protein metadata?"))
print()
print(generate_answer("How does the classifier handle Chinese hamster ovary cell proteins?"))

"""
Q1. temperature=0.1 is deliberately low. Why does that matter specifically for a RAG answer, as opposed to
something like a creative-writing prompt where you might want temperature=0.9?
Answer: RAG needs the LLM to report what is in the retrieved context, not to be creative or vary its phrasing
across runs. A high temperature (like 0.9) would let the model improvise, paraphrase loosely, or occasionally
drift toward saying something that sounds plausible but is not actually grounded in the context. Low temperture
keeps the model close to a deterministic "read and report" behavior.
Q2. The prompt explicitly says "using ONLY the context" and "if the context doesn't contain the answer,
say so explicitly." What specific failure mode is that instruction defending against, and why isn't the
rerank threshold alone (step 3) sufficient protection against it?
Answer: The threshold gate protects against the irrelevant case; no chunk clears the bar, so the LLM never even gets called.
But it does nothing to stop the LLM from hallucinating on top of context that did pass the gate. Even with genuinely relevant
chunks in hand, an ungrounded LLM can still pad its answer with invented specifics not actually present in the text.
The prompt instruction is the second, independent layer of defense, it constrains what the model does once it has real context,
which the threshold gate cannot touch.
Q3. For the hamster question specifically — did the threshold gate catch it and return the canned refusal,
or did it reach the LLM anyway and get an answer? Either way, explain why, based on the actual reranker scores you saw in rag_cross_encoder_reranker.
Answer: Yes, It was caught cleanly by the threshold gate, not the LLM. This is based on the output we got "I don't have information about that in
the document.", the function returns that on line 'if top_score < rerank_threshold: return...', before Groq is ever called. This matches what we
saw in rag_cross_encoder_reranker where all three reranked candidates scored around -11, far below the 0.0 threshold.
"""

