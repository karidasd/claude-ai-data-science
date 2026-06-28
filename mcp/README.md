# Data Science Model Context Protocol (MCP) Server

This directory contains a custom **Model Context Protocol (MCP)** server tailored for Data Science tasks. 

By adding this server to your Claude client (such as Claude Desktop or Claude Code), you grant Claude the ability to:
1. **Explore Schema**: Read local CSV column names and row counts.
2. **Compute Statistics**: Get data distribution, min/max, standard deviation, and missing values.
3. **Execute Python Sandboxed Code**: Run pandas data manipulation, calculations, or models directly on your system.

---

## 🛠️ Server Setup

### 1. Install Prerequisites
Make sure you have python package dependencies installed:
```bash
pip install mcp[cli] pandas numpy matplotlib
```

### 2. Run and Test Locally
You can test the MCP server in developer inspector mode using the MCP CLI tool. Run this in your terminal:
```bash
mcp dev C:/Users/karid/.gemini/antigravity/scratch/claude-ai-data-science/mcp/ds_mcp_server.py
```
This will start a local inspector UI in your web browser where you can manually invoke and test the server's tools (`read_csv_columns`, `get_column_stats`, `execute_python_code`).

---

## 💻 Configuration

### A. Integrating with Claude Desktop
To give your Claude Desktop application access to these tools, add the configuration below to your settings file.

*   **File Path**: `%APPDATA%\Claude\claude_desktop_config.json` (Open Windows Run `Win + R`, paste `%APPDATA%\Claude` and search for or create `claude_desktop_config.json`).
*   **Configuration Content**:
    ```json
    {
      "mcpServers": {
        "data-science-mcp": {
          "command": "python",
          "args": [
            "C:/Users/karid/.gemini/antigravity/scratch/claude-ai-data-science/mcp/ds_mcp_server.py"
          ],
          "env": {
            "PYTHONUNBUFFERED": "1"
          }
        }
      }
    }
    ```

After saving the configuration, restart your Claude Desktop app. You should see a new hammer icon (tools) representing the data science tools.

### B. Integrating with Claude Code
If you are using Anthropic's developer terminal tool (Claude Code), you can launch it with this MCP server active:
```bash
claude --mcp python C:/Users/karid/.gemini/antigravity/scratch/claude-ai-data-science/mcp/ds_mcp_server.py
```
This will allow the Claude Code agent to directly run data operations on your files while you chat in the terminal.
