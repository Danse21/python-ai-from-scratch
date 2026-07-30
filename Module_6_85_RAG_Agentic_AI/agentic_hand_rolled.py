# Hand-rolled tool-calling agent
# An "agent" is an LLM given a menu of functions it's allowed to request, plus a loop that actually
# executes whatever it asks for and hands the result back.

import json, sqlite3, os, sys
os.environ["HF_HUB_OFFLINE"] = "1"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH
from rag_complete_pipeline import generate_answer, client
from groq import BadRequestError

tools_schema = [
  {
    "type": "function",
    "function": {
      "name": "get_protein_info",
      "description": "Look up a protein's metadata from the local database by Uniprot ID",
      "parameters": {
        "type": "object",
        "properties": {
          "uniprot_id": {"type": "string", "description": "Uniprot accession ID, e.g. P00533"}
        },
        "required": ["uniprot_id"],
      },
    },
  },
  {
    "type": "function",
    "function": {
      "name": "search_documentation",
      "description": "Answer questions about how this project works (API endpoints, database, Docker setup, assumptions) by searching its README. \
      Use the user's original question as closely as possible, without rewording it.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string", "description": "The question to search the documentation for"}
        },
        "required": ["query"],
      },
    },
  },
]

def get_protein_info(uniprot_id: str) -> str:
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM drug_targets WHERE uniprot_id = ?", (uniprot_id,))
  row = cursor.fetchone()
  conn.close()
  if row is None:
    return f"No protein found with ID {uniprot_id}"
  return f"Protein {row[0]}: {row[1]}, gene {row[2]}, organism {row[3]}"

def search_documentation(query: str) -> str:
  return generate_answer(query)    # reuse generate_answer() from rag_complete_pipeline.py

available_functions = {
  "get_protein_info": get_protein_info,
  "search_documentation": search_documentation,
}

def run_agent(user_message: str, max_entries: int = 4) -> str:
  messages = [
    {"role": "system", "content": (
      "You are an assistant for a protein classification project. \
      ALWAYS call get_protein_info when the user asks about a specific protein by ID or accession number (e.g. P00533), \
      even if you already know general facts about it, the local database is the authoritative source, not your training knowledge. \
      Only answer general questions directly. When you receive a tool result, answer using ONLY the information in that tool result. \
      Do not add extra facts from your own general knowledge. If the tool result says no information was found, \
      tell the user honestly that the information isn't available, do not invent an answer."
    )},
    {"role": "user", "content": user_message},
  ]

  for attempt in range(max_entries):
    try:
      response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools_schema,
        tool_choice="auto",
        temperature=0.1,
      )
      break
    except BadRequestError:
      if attempt == max_entries - 1:
        return generate_answer(user_message)
      continue


  response_message = response.choices[0].message
  tool_calls = response_message.tool_calls
  # print(f"DEBUG: tool_calls = {tool_calls}")

  if not tool_calls:
    return response_message.content    # Let model answer directly, no tool needed

  messages.append(response_message)

  for tool_call in tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    result = available_functions[name](**args)
    # print(f"DEBUG: tool result for {name} = {result!r}")

    messages.append({
      "role": "tool",
      "tool_call_id": tool_call.id,
      "name": name,
      "content": result,
    })

  final = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.1)
  return final.choices[0].message.content

if __name__ == "__main__":
  print(run_agent("What can you tell about protein P00533?"))
  print()
  print(run_agent("What database does this project use?"))
  print()
  print(run_agent("What's the capital of Sweden?"))
  # print(get_protein_info("P00533"))

"""
Reflection Question
Q1. For the first query, which tool did the model choose to call, and how could you tell from the code (not just the printed answer)?
Answer:The tool model call is the get_protein_info(). And code-level way to know which tool was called is by debugging:
print(f"DEBUG: tool_calls = {tool_calls}"), specifically tool_call.function.name, which gives name='get_protein_info'.
Q2. The third query ("capital of Sweden") has nothing to do with either tool. What did run_agent actually do with it, and which line in
the code made that possible?
Answer: if not tool_calls:
          return response_message.content
Q3. This is the exact loop LangChain's AgentExecutor would run for you automatically. Now that you've written it by hand, what
specifically do you think a framework like LangChain is saving you from re-writing every time you build a new agent?
Answer:The LangChain's AgentExecutor saves you from rewriting the
entire orchestration protocol you just spent the last dozen messages debugging: building and appending messages with the
correct roles (system/user/assistant/tool), parsing JSON arguments safely, mapping function names to real callables, retrying on
malformed generations, and deciding when to stop versus continue. There's also a real capability gap worth naming: your
hand-rolled version only does one round: call a tool, get a result, generate a final answer. It can't currently handle a
case where, after seeing the first tool's result, the model decides it needs to call a second tool before it can answer.
A real AgentExecutor loops until the model stops requesting tools, however many rounds that takes. That multi-step looping is
probably the single biggest thing you're about to see LangChain hand you for free.
"""
