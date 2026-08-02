import time
from agentic_langChain import agent
from groq import BadRequestError
from rag_complete_pipeline import generate_answer

def ask_with_metrics(question: str, max_retries: int = 4) -> dict:
  start = time.time()
  attempts = 0
  fell_back = False

  for attempt in range(max_retries):
    attempts += 1
    try:
      result = agent.invoke({"messages": [{"role": "user", "content": question}]})
      answer = result["messages"][-1].content
      break
    except BadRequestError:
      if attempt == max_retries - 1:
        answer = generate_answer(question)
        fell_back = True
        continue

  latency = time.time() - start

  return {
    "question": question,
    "answer": answer,
    "attempts": attempts,
    "fell_back_to_rag": fell_back,
    "latency_seconds": round(latency, 2),
  }

test_questions = [
  "What can you tell about protein P00533?",
  "What database does this project use?",
  "What's the capital of Sweden?",
  "How do you run this project with Docker?",
  "What amino acids does the API accept?",
]

results = [ask_with_metrics(q) for q in test_questions]

for r in results:
  print(f"[{r['latency_seconds']}s, {r['attempts']} attempt(s){', FELL BACK' if r['fell_back_to_rag'] else ''}] {r['question']}")

failure_rate = sum(r["fell_back_to_rag"] for r in results) / len(results)
avg_latency = sum(r["latency_seconds"] for r in results) / len(results)
print(f"\nTool-call failure rate: {failure_rate:.0%}")
print(f"Average latency: {avg_latency:.2f}s")

"""
Reflection questions
Q1. Given what you've now observed across many runs, is a tool_use_failed rate anywhere near what you measure
here acceptable for a real product, or would this need to improve before shipping? What would you actually
do about it?
Answer: A single clean run at 0% is not enough evidence to decide for a production-ready. Before deciding one
should diagnose for any failure pattern, check the code again for any bug or model-level issue. Before actually shipping,
one needs to run a much larger and more varied test set, and repeated runs to check for run-to-run variance.
Q2. This script measures failure rate and latency — but not cost. Groq bills per token. What would you need to
add to this function to track cost per query, and why would a company like Etraveli care about that number specifically?
Answer: The function to add to track cost per query would be `response.usage.total_tokens` (or `prompt_tokens`/
`completion_tokens` separately) added to `ask_with_metrics`, multiply by the per token rate for whichever model
you're using, and track it per query. A company like Etraveli cares about this specifically because failure rate
and latency tell you if a system works, but cost tells you if it's worth running at the scale they need. An agent
that is reliable and fast but burns unsustainable tokens per query on a high-volume travel platform is still a
shipping blocker.
"""
