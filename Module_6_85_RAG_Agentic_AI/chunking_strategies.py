# A document split by fixed character count cut sentences and ideas in
# half at arbitrary boundaries. The resulting separate chunks cannot retrieve
# correctly for a question about it.

import re

def chunk_naive(text: str, chunk_size: int = 200) -> list[str]:
  """Splits by raw character count, ignores sentence/paragraph boundaries."""
  return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def chunk_recursive(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
  """Recursive splitting with overlap: Splits on paragraph breaks first, falling back to
  sentence if a paragraph is still too long. Adjacent chunks share `overlap` characters so
  an idea split across a boundary isn't lost from either chunk"""
  paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
  chunks = []
  current = ""
  for para in paragraphs:
    if len(current) + len(para) <= chunk_size:
      current += para + "\n\n"
    else:
      if current:
        chunks.append(current.strip())

      # paragraph itself too long, split on sentenecs
      if len(para) > chunk_size:
        sentences = re.split(r'(?<=[.!?])\s+', para)
        current = ""
        for sent in sentences:
          if len(current) + len(sent) <= chunk_size:
            current += sent + " "
          else:
            chunks.append(current.strip())
            current = sent + " "
      else:
        current = para + "\n\n"
  if current:
    chunks.append(current.strip())

  # add overlap between adjacent chunks
  overlapped = []
  for i, chunk in enumerate(chunks):
    if i > 0:
      prev_tail = chunks[i-1][-overlap:]
      chunk = prev_tail + " " + chunk
    overlapped.append(chunk)
  return overlapped

# Run on this repo's README.md
with open("README.md") as f:
  readme = f.read()
naive_chunks = chunk_naive(readme)
recursive_chunks = chunk_recursive(readme)

print(f"Naive: {len(naive_chunks)} chunks")
print(f"Recursive: {len(recursive_chunks)} chunks")
print("\n...Naive chunk 2...")
print(naive_chunks[1])
print("\n...Recursive chunk 2...")
print(recursive_chunks[1])


"""
Reflection question:
Q1. Look at naive_chunks[1] — does it start or end mid-word or mid-sentence? Why does that matter for retrieval later, specifically?
Answer: The output of naive_chunks[1] starts mid-word in a mid-sentence and ends the same, mid-word in a truncated sentence. This matters for
retrieval later because cut words and sentences result to loss of vital information needed in the chunk to retrieve correctly for a question about it.
Q2. Why does chunk_recursive add overlap between chunks instead of leaving clean, non-overlapping boundaries? What real failure does the overlap prevent?
Answer: This is to ensure that an ideas or vital part of a sentence is not lost in chunk split across a boundary, which the overlap tries to prevent.
The overlap's real job is to guarantee that even if a boundary lans mid-idea, at least one chunk still contains that idea intact (the tail of chunk N
gets copied to the start of chunk N+1), so retrieval has a real chance of finding it.
Q3. Your README.md has distinct sections (Project Architecture, Endpoints, Assumptions). If a user asks "what does the API assume about dataset used for model training?",
which chunking approach is more likely to retrieve a chunk containing the complete answer, and why?
Answer: The Most appropriate chunk approach will be chunk_recursive. This is because chunk_recursive splits on paragraph/section boundaries ("\n\n") before
falling back to raw character counts, so the whole "Assumptions" section, including the small dataset classifier was trained bullet, tends to stay
together as one topically coherent chunk. Naive chunking, on the other hand, does arbitrary or random splitting resulting to chunking of unrelated things.
Overlap is the safety net and paragrap-aware splitting is the main mechanism.
"""
