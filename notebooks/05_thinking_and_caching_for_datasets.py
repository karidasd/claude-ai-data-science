# %% [markdown]
# # Advanced Claude Features: Extended Thinking & Prompt Caching
# This script covers how to use Claude's **Prompt Caching** (to reuse large datasets efficiently)
# and **Extended Thinking Mode** (for complex reasoning, mathematical modeling, and code analysis).
#
# Aligns with **Building with the Claude API (Prompt Caching & Thinking)** guidelines.
#
# ## Objectives:
# 1. Learn to enable Prompt Caching for datasets to reduce API cost/latency.
# 2. Learn to enable Extended Thinking Mode for complex reasoning.

# %%
import os
import pandas as pd
from anthropic import Anthropic

# %%
# Initialize Client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key if api_key else "YOUR_API_KEY_HERE")
MODEL_NAME = "claude-3-5-sonnet-latest" # Prompt Caching and Thinking are fully supported

# %% [markdown]
# ## 1. Prompt Caching
# When you supply large datasets (like 50,000 rows of CSV data) repeatedly, you pay for input tokens every single request.
# Anthropic Prompt Caching allows you to cache static blocks of text. Subsequent calls that hit the cache cost 90% less and load instantly.
# 
# To cache a message block, add `cache_control={"type": "ephemeral"}`.

# %%
# Imagine this is a large CSV dataset (e.g. sales logs)
large_dataset_mock = """
Date,Product,Category,Revenue,UnitsSold
2026-01-01,Product_A,Electronics,1200.50,12
2026-01-02,Product_B,Apparel,450.00,3
2026-01-02,Product_A,Electronics,2401.00,24
2026-01-03,Product_C,Home,89.90,1
... (imagine 5,000 lines of data here) ...
"""

# We can cache the system prompt and the dataset block.
cached_messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"Here is the database snapshot that I will ask multiple questions about:\n\n{large_dataset_mock}",
                # Enable caching on this block by setting cache_control
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": "First Question: Which category generated the highest total revenue?"
            }
        ]
    }
]

# %% [markdown]
# ## 2. Extended Thinking Mode
# For complex mathematical modeling, feature engineering decisions, or debugging deep learning architectures,
# Claude benefits from a "thinking budget" where it reasons step-by-step in a private thought process before replying.
#
# Note:
# - Set `thinking={"type": "enabled", "budget_tokens": 1024}`.
# - Set `max_tokens` higher than `budget_tokens` (e.g., 2048 or 4096) to accommodate both thinking and output.

# %%
try:
    if api_key:
        print("Calling Claude with Extended Thinking Mode enabled...")
        
        # Define a complex reasoning prompt for Data Scientists
        complex_prompt = (
            "We have a binary classification task where the positive class is only 1.2% of the dataset. "
            "Explain the pros and cons of using Random Forest vs. XGBoost vs. Logistic Regression in this scenario, "
            "and propose a detailed validation and evaluation strategy that prevents data leakage and metric bias."
        )
        
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096, # High max_tokens is required when thinking is enabled
            thinking={
                "type": "enabled",
                "budget_tokens": 2048 # Number of tokens allocated for internal reasoning
            },
            messages=[
                {"role": "user", "content": complex_prompt}
            ]
        )
        
        # Display the thinking blocks if they exist in the response
        print("\n=== CLAUDE'S INTERNAL THINKING PROCESS ===")
        for block in response.content:
            if block.type == "thinking":
                print(block.thinking)
                
        # Display the final output text block
        print("\n=== CLAUDE'S FINAL RECOMMENDATION ===")
        for block in response.content:
            if block.type == "text":
                print(block.text)
                
    else:
        print("\n(Skipping API call because ANTHROPIC_API_KEY is not set).")
        print("Thinking Mode Configuration Example:")
        print("""
response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 2048
    },
    messages=[...]
)
        """)
        
except Exception as e:
    print(f"\nExecution failed: {e}")
