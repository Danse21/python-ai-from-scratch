# The @tool decorator reads function's docstring and type hints to build the schema automatically.
# create_agent builds and runs tool-calling loop, including looping back for a second round of tool calls
# if the model decides it needs one.
# Invocation takes a 'message' list and returns a state dict; the final answer is 'result["message"][-1].content

import sqlite3, os, sys, re
os.environ["HF_HUB_OFFLINE"] = "1"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
from config import DB_PATH
from groq import BadRequestError
from rag_complete_pipeline import generate_answer

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.1)

@tool
def get_protein_info(uniprot_id: str) -> str:
  """Look up a protein's metadata from the local database by Uniprot ID."""
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM drug_targets WHERE uniprot_id = ?", (uniprot_id,))
  row = cursor.fetchone()
  conn.close()
  if row is None:
    return f"No protein found with ID {uniprot_id}"
  return f"Protein {row[0]}: {row[1]}, gene {row[2]}, organism {row[3]}"

@tool
def search_documentation(query: str) -> str:
  """Answer questions about how this project works (API endpoints, database, Docker setup, assumptions) \
    by searching its README. Use the user's original question as closely as possible."""
  return generate_answer(query)

system_prompt = (
    "You are an assistant for a protein classification project. \
    ALWAYS call get_protein_info when the user asks about a specific protein by ID or accession number (e.g. P00533), \
    even if you already know general facts about it, the local database is the authoritative source, not your training knowledge. \
    Only answer general questions directly. When you receive a tool result, answer using ONLY the information in that tool result. \
    Do not add extra facts from your own general knowledge. If the tool result says no information was found, \
    tell the user honestly that the information isn't available, do not invent an answer."
  )

agent = create_agent(llm, tools=[get_protein_info, search_documentation], system_prompt=system_prompt)

UNIPROT_PATTERN = re.compile(r'\b[A-Z][0-9][A-Z0-9]{3}[0-9]\b')

def ask_with_fallback(question: str, max_retries: int = 4) -> str:
  for attempt in range(max_retries):
    try:
      result = agent.invoke({"messages": [{"role": "user", "content": question}]})
      return result["messages"][-1].content
    except BadRequestError:
      if attempt == max_retries - 1:
        match = UNIPROT_PATTERN.search(question)
        if match:
          print(f"DEBUG: fell back to direct DB lookup for {match.group()}")   # show the Query 1 output is not LLM response but rather database call by uniprot pattern match.
          return get_protein_info.invoke({"uniprot_id": match.group()})    # direct DB lookup, no LLM needed
        return generate_answer(question)    # fall back to RAG if no protein ID is detected
      continue

if __name__ == "__main__":
  print(ask_with_fallback("What can you tell about protein P00533?"))
  print()
  print(ask_with_fallback("What database does this project use?"))
  print()
  print(ask_with_fallback("What's the capital of Sweden?"))
