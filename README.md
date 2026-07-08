 Pro Data Agent — AI Data Analyst Agent

Show Image
Show Image
Show Image
Show Image

An autonomous AI agent that acts like a mini data analyst. Upload a CSV, chat with it in plain English, and it filters, cleans, analyzes, and visualizes your data — powered by Google's Gemini API.

This is a "Digital FTE" style project: an AI agent that takes a specific user input, reasons about it, and performs a real automated task (not just chatting) — generating and safely executing pandas/Plotly code on real data.


📸 Demo

<!-- Replace this with an actual screenshot or GIF of your app once deployed -->
<!-- Example: ![App Screenshot](screenshots/main-view.png) -->

🖼️ Screenshot coming soon — add an image of the app here (e.g. screenshots/main-view.png)



Data Quality ReportChat InteractionChart Generationscreenshot herescreenshot herescreenshot here

🔗 Live demo: [Add your Hugging Face Space / deployed link here]


✨ Features


💬 Chat-based interface — describe what you want in plain English, get results in a conversation
🔍 Filter & analyze — "show only Punjab customers", "average revenue by region", "which region has the highest revenue"
🧹 Clean permanently, when asked — "remove duplicates permanently", "fill missing revenue with the average" — the agent distinguishes between a temporary view and a permanent change, so casual questions never silently corrupt your data
📊 Visualize — bar charts, pie charts, histograms, scatter plots, generated via Plotly from natural language
🧪 Auto Data Quality Report — the moment you upload a file, instantly see duplicate rows, missing values per column, and dtypes — no AI call needed
↩️ Reset button — snap back to your original uploaded data at any time
🔎 Transparent code generation — every AI-generated snippet is shown in an expander so you can see exactly what ran
🛡️ Sandboxed execution — generated code is checked against a deny-list (no import, exec, eval, file/OS access) before running



🏗️ Architecture

CSV upload
     ↓
Auto data quality report (pandas only, instant)
     ↓
User instruction (plain English, via chat)
     ↓
Gemini generates pandas/plotly code
     ↓
Code safety check (deny-list) + sandboxed execution
     ↓
Keyword gate: does the instruction actually ask for a
PERMANENT change (e.g. "remove duplicates permanently")?
   → No  → treated as a VIEW: displayed only, dataset unchanged
   → Yes → working dataset is updated
     ↓
Result (table/chart) shown in chat + persisted across reruns


🚀 Getting Started

Prerequisites


Python 3.9+
A free Gemini API key (no credit card required)


Installation

bashgit clone https://github.com/iqrabatool1/ai-data-analyst-agent.git
cd ai-data-analyst-agent
pip install -r requirements.txt

Run

bashstreamlit run app.py

Paste your Gemini API key into the sidebar, upload a CSV, and try prompts like:

Filter rows where revenue > 5000
Bar chart of total revenue by region
Remove duplicate rows permanently
Fill missing revenue with the average, permanently


🛠️ Tech Stack

LayerTechnologyUI / App frameworkStreamlitData handlingpandasVisualizationPlotly ExpressAI reasoningGoogle Gemini APILanguagePython


📁 Project Structure

ai-data-analyst-agent/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── sample_data.csv     # Example dataset for testing
├── .gitignore
└── README.md


⚠️ Safety Notes

Generated code runs through exec() in a restricted namespace (limited builtins, no import/os/sys/file access). This is a reasonable safeguard for a learning/portfolio project, but for production use, a true sandboxed subprocess or container-based execution would be more robust.


🗺️ Roadmap


 Undo history (multi-step, not just reset-to-original)
 Export full session as a Word/PDF report
 Multi-file support with joins
 Auto-retry when generated code errors out



🙋 About This Project

Built as a hands-on exploration of AI agent architecture — the core loop of input → reasoning → tool execution → output — applied to a real data analyst use case. Combines interests in AI agents and data analytics into one working tool.
