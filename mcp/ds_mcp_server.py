# %%
# Data Science MCP (Model Context Protocol) Server
# This server exposes tools to let Claude interact with local datasets, compute statistics,
# and run Python code for exploratory data analysis.
#
# It aligns with the "Introduction to MCP" and "MCP: Advanced Topics" courses from Anthropic Academy.

import os
import sys

# Ensure required packages are present
try:
    from mcp.server.fastmcp import FastMCP
    import pandas as pd
    import numpy as np
except ImportError:
    print("WARNING: Required libraries (mcp, pandas, numpy) are not installed.")
    print("Please install them using: pip install mcp[cli] pandas numpy matplotlib")

# Create the FastMCP instance
mcp = FastMCP("Data Science Server")

# %% [markdown]
# ## Tool 1: Read CSV Column Names

@mcp.tool()
def read_csv_columns(file_path: str) -> str:
    """
    Reads a CSV file from a local path and returns its shape and column names.
    Use this tool first to understand the schema of a dataset.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    try:
        df = pd.read_csv(file_path, nrows=5)
        # Get shape without reading the full file into memory immediately
        rows_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')) - 1
        cols = list(df.columns)
        return f"Dataset: {file_path}\nTotal Rows: {rows_count}\nColumns: {cols}"
    except Exception as e:
        return f"Error reading CSV schema: {str(e)}"

# %% [markdown]
# ## Tool 2: Get Summary Statistics

@mcp.tool()
def get_column_stats(file_path: str, column_name: str) -> str:
    """
    Computes summary statistics (mean, median, standard deviation, null counts, etc.)
    for a specific numerical or categorical column in a local CSV dataset.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    try:
        # Read only the target column to save memory
        df = pd.read_csv(file_path, usecols=[column_name])
        desc = df[column_name].describe()
        null_count = df[column_name].isnull().sum()
        
        output = f"Summary Statistics for column '{column_name}':\n"
        output += desc.to_string()
        output += f"\nNull Values count: {null_count}"
        return output
    except ValueError:
        return f"Error: Column '{column_name}' not found in the file."
    except Exception as e:
        return f"Error analyzing column: {str(e)}"

# %% [markdown]
# ## Tool 3: Execute Python Sandbox Code

@mcp.tool()
def execute_python_code(code: str) -> str:
    """
    Executes a short Python snippet inside a local sandbox containing pandas, numpy, and matplotlib.
    Use this to run data filtering, aggregations, and generate visualizations.
    Return any outputs via print() statements.
    """
    from io import StringIO
    
    # Save standard output and redirect it to capture outputs
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    # Setup execution context
    context = {
        "pd": pd,
        "np": np,
        "sys": sys
    }
    
    try:
        # Execute python snippet
        exec(code, context)
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return f"Runtime Error during execution: {str(e)}"

# %% [markdown]
# ## Run Server
# When executed directly, the FastMCP server runs on stdio transport.

if __name__ == "__main__":
    # Check if run via command line
    mcp.run()
