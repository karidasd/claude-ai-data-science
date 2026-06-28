# Claude AI & Data Science Integration

Welcome to the **Claude AI & Data Science Integration** repository! This project bridges the gap between Anthropic's official Claude educational materials and real-world Data Science and AI Engineering workflows. 

It is designed to "marry" AI capabilities with data science practices, demonstrating how Claude can act as an intelligent partner for data cleaning, exploratory data analysis (EDA), predictive modeling, research RAG (Retrieval-Augmented Generation), and custom tool execution.

---

## 📚 Anthropic Academy: All 13 Courses at a Glance

Here is a curated overview of all official free courses offered by [Anthropic Academy](https://anthropic.skilljar.com/), complete with direct links to enroll, target audience, and prerequisite requirements.

| Course | Direct Enrollment Link | Who It's For | Coding? | Prerequisites |
| :--- | :--- | :--- | :--- | :--- |
| **Claude 101** | [Enroll here](https://anthropic.skilljar.com/claude-101) | Everyone | No | None |
| **AI Fluency: Framework & Foundations** | [Enroll here](https://anthropic.skilljar.com/ai-fluency-framework-foundations) | Everyone | No | None |
| **AI Fluency for Students** | [Enroll here](https://anthropic.skilljar.com/ai-fluency-for-students) | Students | No | None |
| **AI Fluency for Educators** | [Enroll here](https://anthropic.skilljar.com/ai-fluency-for-educators) | Educators | No | None |
| **Teaching AI Fluency** | [Enroll here](https://anthropic.skilljar.com/teaching-ai-fluency) | Instructional designers | No | AI Fluency basics |
| **AI Fluency for Nonprofits** | [Enroll here](https://anthropic.skilljar.com/ai-fluency-for-nonprofits) | Nonprofits | No | AI Fluency basics |
| **Building with the Claude API** | [Enroll here](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | Developers | Python | JSON basics |
| **Claude Code in Action** | [Enroll here](https://anthropic.skilljar.com/claude-code-in-action) | Developers | CLI | Git basics |
| **Introduction to Agent Skills** | [Enroll here](https://anthropic.skilljar.com/introduction-to-agent-skills) | Developers | Markdown | Claude Code experience |
| **Introduction to MCP** | [Enroll here](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | Developers | Python | JSON & HTTP basics |
| **MCP: Advanced Topics** | [Enroll here](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) | Developers | Python | MCP intro + async |
| **Claude with Amazon Bedrock** | [Enroll here](https://anthropic.skilljar.com/claude-in-amazon-bedrock) | Developers | Python | AWS basics |
| **Claude with Google Vertex AI** | [Enroll here](https://anthropic.skilljar.com/claude-with-google-vertex) | Developers | Python | GCP basics |

---

## 🎯 Data Science Learning Paths

To make the most of these courses in a Data Science context, we recommend the following learning tracks:

### Path A: The Citizen Data Scientist (No-code / Analyst)
*Learn to leverage Claude via the web interface to speed up data exploration and reporting.*
1. **Claude 101** $\rightarrow$ Master prompt basics and document uploads.
2. **AI Fluency: Framework & Foundations** $\rightarrow$ Understand AI limitations, hallucination risks, and when human oversight is mandatory.

### Path B: The AI & Data Engineer (Coding / Integration)
*Build AI-driven pipelines, automate exploratory data analysis, and deploy custom tools for Claude.*
1. **Building with the Claude API** $\rightarrow$ Understand system prompts, token caching, and structured outputs (JSON).
2. **Introduction to MCP** $\rightarrow$ Learn to write Model Context Protocol servers to let Claude query your local databases and CSV files.
3. **Claude Code in Action** $\rightarrow$ Integrate Claude into your terminal workspace to refactor analysis scripts, clean code, and write unit tests.
4. **Introduction to Agent Skills** $\rightarrow$ Build custom `SKILL.md` configurations to guide Claude through your proprietary data workflows.

---

## 📂 Repository Structure

This repository is organized into practical components that apply Anthropic's teachings directly to data science challenges:

*   **`notebooks/`**: Interactive Python scripts (Jupyter `# %%` cell format) containing code walk-throughs:
    *   `01_claude_api_for_data_science.py`: Basics of using the Anthropic API with tabular datasets.
    *   `02_prompt_engineering_for_data_scientists.py`: Structuring data, few-shot prompting, and extracting clean JSON.
    *   `03_tool_use_and_data_agents.py`: Letting Claude call local python functions (e.g. database querying, plot generation).
    *   `04_rag_on_scientific_literature.py`: Building a mini-RAG pipeline to query bioRxiv/arXiv and synthesize research papers.
*   **`mcp/`**: A custom Model Context Protocol (MCP) server designed to give Claude secure tools to interact with local datasets, compute statistics, and render visualizations.
*   **`skills/`**: A custom Agent Skill (`SKILL.md`) that guides agentic tools (like Claude Code) on how to perform automated data science code reviews and exploratory data analysis.
*   **`dashboard/`**: A visually stunning, interactive web dashboard showcasing courses, resources, and custom guides.

---

## 🚀 Local Quickstart

### 1. Prerequisites
Ensure you have Python 3.10+ installed. Install the required dependencies:
```bash
pip install anthropic pandas numpy matplotlib scikit-learn mcp httpx
```

### 2. Configure API Key
Set your Anthropic API Key in your terminal session:
*   **Windows (PowerShell)**:
    ```powershell
    $env:ANTHROPIC_API_KEY="your-api-key-here"
    ```
*   **Linux/macOS**:
    ```bash
    export ANTHROPIC_API_KEY="your-api-key-here"
    ```

### 3. Run the Interactive Scripts
You can open the scripts in the `notebooks/` folder inside any IDE that supports interactive notebooks (like VS Code or PyCharm) and execute them cell by cell.

### 4. Open the Web Dashboard
Navigate to the `dashboard/` directory and open `index.html` in your web browser to explore the curriculum visually.
