# %% [markdown]
# # Tool Use (Function Calling) for Data Science Agents
# This script demonstrates how to equip Claude with tools to perform data calculations 
# and generate plots. It aligns with the **Building with the Claude API (Tool Use)** course.
# 
# ## Objectives:
# 1. Define python helper functions for data calculations and plotting.
# 2. Expose these functions as tools in the Claude API request.
# 3. Handle the model's tool calls and return the results back to Claude.

# %%
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from anthropic import Anthropic

# %%
# Initialize Client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key if api_key else "YOUR_API_KEY_HERE")
MODEL_NAME = "claude-3-5-sonnet-latest"

# %% [markdown]
# ## 1. Prepare Local Data and Functions
# We generate a dataset where `Age` and `Income` are correlated.

# %%
np.random.seed(42)
ages = np.random.randint(22, 65, 50)
incomes = ages * 1500 + np.random.normal(0, 10000, 50)

df = pd.DataFrame({
    "Age": ages,
    "Income": incomes
})

# Define the local tool functions
def calculate_correlation(col1: str, col2: str) -> str:
    """Calculates Pearson correlation coefficient between two columns."""
    if col1 not in df.columns or col2 not in df.columns:
        return f"Error: Columns must be one of {list(df.columns)}"
    corr = df[col1].corr(df[col2])
    return json.dumps({"correlation": float(corr), "col1": col1, "col2": col2})

def generate_scatter_plot(col_x: str, col_y: str) -> str:
    """Generates a scatter plot and saves it to scatter_plot.png."""
    if col_x not in df.columns or col_y not in df.columns:
        return f"Error: Columns must be one of {list(df.columns)}"
    
    plt.figure(figsize=(6, 4))
    plt.scatter(df[col_x], df[col_y], color="indigo", alpha=0.7)
    plt.title(f"{col_x} vs {col_y}")
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.grid(True, linestyle="--", alpha=0.6)
    
    output_filename = "scatter_plot.png"
    plt.savefig(output_filename, dpi=150, bbox_inches="tight")
    plt.close()
    return json.dumps({"status": "success", "saved_image": output_filename})

# %% [markdown]
# ## 2. Define Tools for the API
# We must declare our tools using the Anthropic tool schema.

# %%
tools_schema = [
    {
        "name": "calculate_correlation",
        "description": "Calculates the Pearson correlation coefficient between two columns of the local dataset.",
        "input_schema": {
            "type": "object",
            "properties": {
                "col1": {
                    "type": "string",
                    "description": "The name of the first column (e.g. 'Age')."
                },
                "col2": {
                    "type": "string",
                    "description": "The name of the second column (e.g. 'Income')."
                }
            },
            "required": ["col1", "col2"]
        }
    },
    {
        "name": "generate_scatter_plot",
        "description": "Generates a scatter plot comparing two numerical columns and saves it as an image.",
        "input_schema": {
            "type": "object",
            "properties": {
                "col_x": {
                    "type": "string",
                    "description": "Column name for the X-axis."
                },
                "col_y": {
                    "type": "string",
                    "description": "Column name for the Y-axis."
                }
            },
            "required": ["col_x", "col_y"]
        }
    }
]

# %% [markdown]
# ## 3. Executing the Tool Loop
# In agentic workflows, if the model decides it needs a tool, it returns a `tool_use` block. 
# We run the function locally, and send the output back as a `tool_result` message.

# %%
user_prompt = "Can you check if there is a strong correlation between Age and Income in my data, and generate a plot for it?"

try:
    if api_key:
        print("Sending initial prompt to Claude...")
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1000,
            tools=tools_schema,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        print("\nClaude's stop reason:", response.stop_reason)
        
        # Check if Claude wants to use tools
        tool_calls = [content for content in response.content if content.type == "tool_use"]
        
        if tool_calls:
            print(f"\nClaude decided to call {len(tool_calls)} tools:")
            
            # We must maintain the conversation history
            conversation_history = [
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": response.content}
            ]
            
            tool_results_content = []
            
            for tool_call in tool_calls:
                tool_name = tool_call.name
                tool_input = tool_call.input
                tool_id = tool_id = tool_call.id
                
                print(f"- Tool: {tool_name} with input {tool_input}")
                
                # Execute tool locally
                if tool_name == "calculate_correlation":
                    result = calculate_correlation(tool_input["col1"], tool_input["col2"])
                elif tool_name == "generate_scatter_plot":
                    result = generate_scatter_plot(tool_input["col_x"], tool_input["col_y"])
                else:
                    result = "Error: Tool not found."
                
                # Construct tool response block
                tool_results_content.append({
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result
                })
            
            # Send the tool results back to Claude
            conversation_history.append({
                "role": "user",
                "content": tool_results_content
            })
            
            print("\nSending tool execution results back to Claude...")
            final_response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=1000,
                tools=tools_schema,
                messages=conversation_history
            )
            
            print("\n=== CLAUDE'S FINAL ANALYSIS ===")
            print(final_response.content[0].text)
            
except Exception as e:
    print(f"\nExecution failed: {e}")
