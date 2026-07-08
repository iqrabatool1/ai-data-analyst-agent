Pro Data Agent — AI Data Analyst Agent

An autonomous AI agent that acts like a mini data analyst. Upload a CSV, chat with it in plain English, and it filters, cleans, analyzes, and visualizes your data — powered by Google's Gemini API.

This is a "Digital FTE" style project: an AI agent that takes a specific user input, reasons about it, and performs a real automated task (not just chatting) — generating and safely executing pandas/Plotly code on real data.

✨ Features


Chat-based interface — describe what you want in plain English, get results in a conversation
Filter & analyze — "show only Punjab customers", "average revenue by region", "which region has the highest revenue"
Clean permanently, when asked — "remove duplicates permanently", "fill missing revenue with the average" — the agent distinguishes between a temporary view and a permanent change to your dataset, so casual questions never silently corrupt your data
Visualize — bar charts, pie charts, histograms, scatter plots, generated via Plotly from natural language
Auto Data Quality Report — the moment you upload a file, it instantly shows duplicate rows, missing values per column, and dtypes — no AI call needed
Reset button — snap back to your original uploaded data at any time
Transparent code generation — every AI-generated snippet is shown in an expander so you can see exactly what ran
Sandboxed execution — generated code is checked against a deny-list (no import, exec, eval, file/OS access) before running


🏗️ How it works (architecture)

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

🚀 Setup

bashpip install -r requirements.txt

Get a free Gemini API key at https://aistudio.google.com/apikey (no credit card required).

▶️ Run

bashstreamlit run app.py

Paste your Gemini API key into the sidebar, upload a CSV, and try prompts like:


Filter rows where revenue > 5000
Bar chart of total revenue by region
Remove duplicate rows permanently
Fill missing revenue with the average, permanently


🛠️ Tech stack


Streamlit — chat UI and web app framework
pandas — data handling
Plotly Express — chart generation
Google Gemini API — natural language → code reasoning


⚠️ Safety notes

Generated code runs through exec() in a restricted namespace (limited builtins, no import/os/sys/file access). This is a reasonable safeguard for a learning/portfolio project, but for production use, a true sandboxed subprocess or container-based execution would be more robust.

🗺️ Roadmap / next steps


 Undo history (multi-step, not just reset-to-original)
 Export full session as a Word/PDF report
 Multi-file support with joins
 Auto-retry when generated code errors out
