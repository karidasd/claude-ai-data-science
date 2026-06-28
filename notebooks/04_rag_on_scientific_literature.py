# %% [markdown]
# # RAG (Retrieval-Augmented Generation) on Scientific Literature
# This script demonstrates how to build a RAG pipeline that fetches recent scientific publications
# from the arXiv API, parses their abstracts, and uses Claude to synthesize and answer questions.
# It aligns with the **Building with the Claude API (RAG)** course.
# 
# ## Objectives:
# 1. Fetch scientific paper metadata from the public arXiv API based on search terms.
# 2. Extract and format the abstracts as context documents.
# 3. Supply the retrieved context to Claude to generate an evidence-backed summary.

# %%
import os
import xml.etree.ElementTree as ET
import httpx
from anthropic import Anthropic

# %%
# Initialize Client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key if api_key else "YOUR_API_KEY_HERE")
MODEL_NAME = "claude-3-5-sonnet-latest"

# %% [markdown]
# ## 1. Fetch Papers from arXiv
# We define a function to query the public arXiv API for papers related to a data science topic.

# %%
def search_arxiv(query: str, max_results: int = 3) -> list:
    """Queries arXiv API and returns a list of dictionaries with title and summary."""
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    
    print(f"Requesting arXiv publications for: '{query}'...")
    response = httpx.get(url)
    if response.status_code != 200:
        print("Failed to fetch papers.")
        return []
        
    # Parse XML response
    root = ET.fromstring(response.text)
    
    # Namespaces
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        papers.append({
            "title": title,
            "summary": summary
        })
    return papers

# %% [markdown]
# ## 2. Search for Data Science Topics
# Let's search for "Physics informed neural networks" or "Genomic Deep Learning".

# %%
search_query = "genomics deep learning"
retrieved_papers = search_arxiv(search_query, max_results=3)

print(f"\nRetrieved {len(retrieved_papers)} papers:")
for i, paper in enumerate(retrieved_papers):
    print(f"\n[{i+1}] {paper['title']}")
    print(f"Summary snippet: {paper['summary'][:150]}...")

# %% [markdown]
# ## 3. Construct Context and Call Claude
# We'll format the retrieved papers inside XML tags so that Claude can refer to them as its knowledge base.

# %%
# Build the context string
context_blocks = []
for i, paper in enumerate(retrieved_papers):
    block = f"""<document index="{i+1}">
<title>{paper['title']}</title>
<abstract>{paper['summary']}</abstract>
</document>"""
    context_blocks.append(block)

documents_context = "\n\n".join(context_blocks)

# %%
# Define system and user prompts
system_prompt = (
    "You are a scientific research assistant. Answer the user's question using ONLY the provided document "
    "abstracts. If the answer cannot be found in the documents, state that you do not have enough information. "
    "Cite the documents you use by referring to their index (e.g. [Document 1])."
)

user_question = f"""
Here are the scientific abstracts:

<context>
{documents_context}
</context>

Question: Summarize the main breakthroughs in applying deep learning to genomics mentioned in these papers, and list any challenges they identify.
"""

# %%
try:
    if api_key and retrieved_papers:
        print("\nCalling Claude to synthesize research...")
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=800,
            system=system_prompt,
            messages=[{"role": "user", "content": user_question}]
        )
        
        print("\n=== CLAUDE RAG SUMMARY ===")
        print(response.content[0].text)
        
    elif not api_key:
        print("\n(Skipping API call because ANTHROPIC_API_KEY is not set).")
        print("Check the prompt we constructed for Claude:\n")
        print(user_question[:500] + "\n... [truncated] ...")
        
except Exception as e:
    print(f"\nExecution failed: {e}")
