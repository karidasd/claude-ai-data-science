# %% [markdown]
# # Claude API Fundamentals for Data Science
# This script covers the basics of using the Anthropic API with Python in a data science workflow.
# It aligns with the **Building with the Claude API** course from Anthropic Academy.
# 
# ## Objectives:
# 1. Initialize the Anthropic client.
# 2. Structure messages (system prompt, user prompt).
# 3. Format and send tabular datasets to Claude.
# 4. Request analytical insights from the model.

# %%
import os
import pandas as pd
from anthropic import Anthropic

# %% [markdown]
# ## 1. Initialize Client
# We retrieve the API key from environment variables. If you haven't set it yet, you can supply it directly or configure it in your terminal.

# %%
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("WARNING: ANTHROPIC_API_KEY environment variable not set. Please set it or run client = Anthropic(api_key='...')")
    # For demonstration, we'll initialize with a placeholder
    client = Anthropic(api_key="YOUR_API_KEY_HERE")
else:
    client = Anthropic(api_key=api_key)

# We'll use the recommended Claude 3.5 Sonnet model
MODEL_NAME = "claude-3-5-sonnet-latest"

# %% [markdown]
# ## 2. Create Dummy Dataset
# Let's create a small pandas DataFrame representing customer churn data to analyze.

# %%
data = {
    "CustomerID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Age": [34, 45, 22, 58, 29, 41, 38, 50],
    "Tenure_Months": [12, 24, 2, 36, 8, 18, 5, 48],
    "MonthlyCharges": [65.5, 80.0, 20.0, 110.5, 45.0, 95.0, 30.0, 115.0],
    "SupportCalls_LastMonth": [1, 0, 4, 2, 5, 1, 3, 0],
    "Churned": ["No", "No", "Yes", "No", "Yes", "No", "Yes", "No"]
}

df = pd.DataFrame(data)
print("Dataset to analyze:")
print(df)

# %% [markdown]
# ## 3. Convert Data to Claude-Readable Format
# Claude handles text. For tabular data, Markdown tables or CSV strings are usually the most token-efficient and understandable formats for the model.

# %%
# Convert the DataFrame to a markdown string
df_markdown = df.to_markdown(index=False)
print("Markdown representation:")
print(df_markdown)

# %% [markdown]
# ## 4. Call the Claude API
# We will define a system prompt that gives Claude the role of an expert Data Scientist, and pass the dataset inside the user prompt.

# %%
system_prompt = (
    "You are an expert Data Scientist. Your task is to analyze the provided dataset, "
    "identify key correlation patterns (specifically related to customer churn), "
    "and suggest 3 actionable business strategies to mitigate churn based on the data."
)

user_message = f"""
Here is the customer dataset:

{df_markdown}

Please analyze this dataset and provide:
1. A summary of the cohort.
2. The key drivers that seem to correlate with customer churn.
3. Your recommended next steps.
"""

try:
    print(f"Sending request to {MODEL_NAME}...")
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    print("\n=== CLAUDE DATA ANALYSIS RESPONSE ===")
    print(response.content[0].text)
    
except Exception as e:
    print("\nAPI Call failed. (This is expected if your ANTHROPIC_API_KEY is not set or invalid).")
    print(f"Error: {e}")
