// Courses dataset definition containing all 13 Anthropic Academy courses
const courses = [
    {
        title: "Claude 101",
        link: "https://anthropic.skilljar.com/claude-101",
        category: "no-code",
        coding: "No Coding Required",
        prereqs: "None",
        desc: "Master the fundamentals of interacting with Claude. Learn system prompt basics, how to write clear instructions, and extract high-quality business outputs without writing a line of code."
    },
    {
        title: "AI Fluency: Framework & Foundations",
        link: "https://anthropic.skilljar.com/ai-fluency-framework-foundations",
        category: "no-code",
        coding: "No Coding Required",
        prereqs: "None",
        desc: "A framework-first course mapping AI capabilities, limitations, and ethical boundaries. Critical for data analysts to decide which analytical tasks to delegate safely."
    },
    {
        title: "AI Fluency for Students",
        link: "https://anthropic.skilljar.com/ai-fluency-for-students",
        category: "no-code",
        coding: "No Coding Required",
        prereqs: "None",
        desc: "Focuses on academic research models, career planning, and leveraging AI for efficient studying and concept syntheses."
    },
    {
        title: "AI Fluency for Educators",
        link: "https://anthropic.skilljar.com/ai-fluency-for-educators",
        category: "no-code",
        coding: "No Coding Required",
        prereqs: "None",
        desc: "Integrating AI models into classroom instruction, managing curriculum planning, and grading assessments effectively."
    },
    {
        title: "Teaching AI Fluency",
        link: "https://anthropic.skilljar.com/teaching-ai-fluency",
        category: "no-code",
        coding: "No Coding Required",
        prereqs: "AI Fluency basics",
        desc: "Designed for corporate educators and curriculum creators to build scenario training models for onboarding teams onto AI workflows."
    },
    {
        title: "AI Fluency for Nonprofits",
        link: "https://anthropic.skilljar.com/ai-fluency-for-nonprofits",
        category: "no-code",
        coding: "No Coding Required",
        prereqs: "AI Fluency basics (recommended)",
        desc: "Learn to build workflows that maximize resource allocation in nonprofit settings using free Claude tiers."
    },
    {
        title: "Building with the Claude API",
        link: "https://anthropic.skilljar.com/claude-with-the-anthropic-api",
        category: "python",
        coding: "Python Coding Required",
        prereqs: "Python & JSON basics",
        desc: "The core course for developers. Cover system prompts, multi-turn loops, token caching, tool calling, and designing multi-agent data analysis routing."
    },
    {
        title: "Claude Code in Action",
        link: "https://anthropic.skilljar.com/claude-code-in-action",
        category: "python",
        coding: "CLI / Git Experience",
        prereqs: "Terminal & Git basics",
        desc: "Understand how Anthropic's agentic command-line interface handles coding tasks, context parsing, and GitHub workflows."
    },
    {
        title: "Introduction to Agent Skills",
        link: "https://anthropic.skilljar.com/introduction-to-agent-skills",
        category: "python",
        coding: "Markdown / CLI",
        prereqs: "Basic Claude Code knowledge",
        desc: "Extend your coding assistants with SKILL.md rules. Create trigger-based logic to auto-run checks during data science operations."
    },
    {
        title: "Introduction to MCP",
        link: "https://anthropic.skilljar.com/introduction-to-model-context-protocol",
        category: "python",
        coding: "Python Coding Required",
        prereqs: "JSON and HTTP basics",
        desc: "Build Model Context Protocol servers to let Claude query databases, inspect file directories, and interact with the local operating system."
    },
    {
        title: "MCP: Advanced Topics",
        link: "https://anthropic.skilljar.com/model-context-protocol-advanced-topics",
        category: "python",
        coding: "Python Coding Required",
        prereqs: "Intro MCP + Async Python",
        desc: "Dive into production concerns: custom LLM sampling, streamable HTTP connections, roots-based permissions, and deploying load balancers."
    },
    {
        title: "Claude with Amazon Bedrock",
        link: "https://anthropic.skilljar.com/claude-in-amazon-bedrock",
        category: "python",
        coding: "Python Coding Required",
        prereqs: "AWS basic knowledge",
        desc: "Run tools, caching, and RAG architectures using AWS Bedrock endpoints and boto3 python libraries."
    },
    {
        title: "Claude with Google Vertex AI",
        link: "https://anthropic.skilljar.com/claude-with-google-vertex",
        category: "python",
        coding: "Python Coding Required",
        prereqs: "GCP basic knowledge",
        desc: "Deploy Claude models within Google Cloud Platform using Google's Vertex SDKs, with advanced vision and document processing capability."
    }
];

// DOM elements
const coursesContainer = document.getElementById("courses-container");
const filterButtons = document.querySelectorAll(".filter-btn");
const navItems = document.querySelectorAll(".nav-item");
const tabPanels = document.querySelectorAll(".tab-panel");

// Prompt Sandbox Elements
const toggleXmlBtn = document.querySelector(".toggle-xml-btn");
const structuredPromptBox = document.getElementById("structured-prompt");
let isXmlApplied = false;

// Copy MCP config
const copyMcpBtn = document.getElementById("copy-mcp-btn");
const mcpCodeBlock = document.getElementById("mcp-code-block");

// Initialisation function
function init() {
    renderCourses("all");
    setupEventListeners();
}

// Render courses list in the grid
function renderCourses(filter) {
    coursesContainer.innerHTML = "";
    
    const filteredCourses = courses.filter(course => {
        if (filter === "all") return true;
        return course.category === filter;
    });

    filteredCourses.forEach(course => {
        const badgeClass = course.category === "no-code" ? "no-code" : "code";
        const cardHtml = `
            <div class="course-card">
                <div class="card-header">
                    <h3>${course.title}</h3>
                    <span class="card-badge ${badgeClass}">${course.coding}</span>
                </div>
                <p>${course.desc}</p>
                <div class="card-meta">
                    <span>Prereqs: ${course.prereqs}</span>
                    <a href="${course.link}" target="_blank" class="enroll-link">
                        Enroll <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            </div>
        `;
        coursesContainer.insertAdjacentHTML("beforeend", cardHtml);
    });
}

// Setup Event Listeners
function setupEventListeners() {
    // Tab switching logic
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetTab = item.getAttribute("data-tab");
            
            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");
            
            tabPanels.forEach(panel => {
                panel.classList.remove("active");
                if (panel.id === `${targetTab}-tab`) {
                    panel.classList.add("active");
                }
            });
        });
    });

    // Course filters logic
    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            filterButtons.forEach(f => f.classList.remove("active"));
            btn.classList.add("active");
            const filterValue = btn.getAttribute("data-filter");
            renderCourses(filterValue);
        });
    });

    // XML Toggle Sandbox simulation
    if (toggleXmlBtn) {
        toggleXmlBtn.addEventListener("click", () => {
            isXmlApplied = !isXmlApplied;
            if (isXmlApplied) {
                structuredPromptBox.innerHTML = `&lt;instructions&gt;
Analyze the customer feedback in the &lt;dataset&gt; block. 
Output your analysis strictly in a valid JSON object matching this schema:
{
  "customer": "string",
  "feedback_summary": "string",
  "rating_stars": integer
}
&lt;/instructions&gt;

&lt;dataset&gt;
The widget broke on first use! Customer name: John Doe. Rating: 1 star.
&lt;/dataset&gt;`;
                toggleXmlBtn.innerText = "Revert to Raw Text";
                toggleXmlBtn.style.background = "var(--accent-purple-gradient)";
                toggleXmlBtn.style.color = "white";
            } else {
                structuredPromptBox.innerText = "Click the button to see structured XML output formatting...";
                toggleXmlBtn.innerText = "Apply XML Structuring";
                toggleXmlBtn.style.background = "var(--accent-gradient)";
                toggleXmlBtn.style.color = "var(--bg-primary)";
            }
        });
    }

    // Copy MCP Config
    if (copyMcpBtn) {
        copyMcpBtn.addEventListener("click", () => {
            navigator.clipboard.writeText(mcpCodeBlock.innerText).then(() => {
                copyMcpBtn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
                setTimeout(() => {
                    copyMcpBtn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy Configuration`;
                }, 2000);
            }).catch(err => {
                console.error("Could not copy text: ", err);
            });
        });
    }

    // Prompt Generator Logic
    const generatePromptBtn = document.getElementById("generate-prompt-btn");
    const taskSelect = document.getElementById("task-select");
    const promptOutputBox = document.getElementById("prompt-output-box");
    const copyPromptBtn = document.getElementById("copy-prompt-btn");

    if (generatePromptBtn && taskSelect && promptOutputBox) {
        generatePromptBtn.addEventListener("click", () => {
            const selectedTask = taskSelect.value;
            const promptTemplate = promptsData[selectedTask];
            promptOutputBox.innerText = promptTemplate;
        });
    }

    if (copyPromptBtn && promptOutputBox) {
        copyPromptBtn.addEventListener("click", () => {
            navigator.clipboard.writeText(promptOutputBox.innerText).then(() => {
                copyPromptBtn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
                setTimeout(() => {
                    copyPromptBtn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy Prompt`;
                }, 2000);
            }).catch(err => {
                console.error("Could not copy prompt: ", err);
            });
        });
    }
}

// Data Science Prompts Data templates
const promptsData = {
    "data-cleaning": `<instructions>
You are a data-cleaning agent. Your task is to clean and prepare the provided CSV dataset.
1. Identify all columns with missing values.
2. For numeric columns, impute missing values with the median.
3. For categorical columns, impute missing values with the mode.
4. Output a summary of imputations made and the final cleaned DataFrame.
</instructions>

<dataset>
[Insert Your CSV Content Here]
</dataset>`,
    "feature-engineering": `<instructions>
You are an expert feature selection agent. Review the columns of the provided dataset and identify which features should be selected or created for predicting the target variable.
1. Compute the correlation of all variables with the target.
2. Recommend feature engineering steps (e.g. log scaling, one-hot encoding).
3. Draft python code using pandas to execute these steps.
</instructions>

<dataset>
Target Column: [Specify Target Column]
Columns Info: [Specify Column Names and Types]
</dataset>`,
    "model-selection": `<instructions>
You are a machine learning evaluation assistant. Analyze the model performance metrics provided.
1. Compare precision, recall, and ROC-AUC scores.
2. Identify if the model is overfitting or underfitting.
3. Suggest 3 hyperparameters to tune to improve generalization performance.
</instructions>

<model_metrics>
[Insert Train/Test Classification Report or Confusion Matrix Here]
</model_metrics>`,
    "data-visualization": `<instructions>
You are a matplotlib expert visualization designer.
Generate clean, production-ready Python plotting code using matplotlib and seaborn to visualize the relationship in the provided data description.
Rules:
- Include axis labels, title, and a grid.
- Use a professional, high-contrast dark palette.
- Set figsize to (8, 5) and save the plot as a high-DPI PNG.
</instructions>

<data_description>
[Insert columns to plot and plot type, e.g. scatter plot of Age vs. Income]
</data_description>`
};

// Start app
window.addEventListener("DOMContentLoaded", init);
