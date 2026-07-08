# 🧮 Pro Data Agent — AI Data Analyst Agent

> **An autonomous AI agent that acts like a mini data analyst.** Upload a CSV, chat with it in plain English, and it filters, cleans, analyzes, and visualizes your data — powered by Google's Gemini API.

This is a "Digital FTE" style project: an AI agent that takes a specific user input, reasons about it, and performs a real automated task (not just chatting) — generating and safely executing pandas/Plotly code on real data.

🔗 **Live Demo:** [Add your Hugging Face Space / deployed link here]

---

## 📸 Demo

<!-- Replace this with an actual screenshot or GIF of your app once deployed -->
<!-- Example: ![App Screenshot](screenshots/main-view.png) -->
🖼️ *Screenshot coming soon — add an image of the app here (e.g. screenshots/main-view.png)*

### Feature Walkthrough Placeholders:
* **Data Quality Report:** (https://github.com/iqrabatool1/ai-data-analyst-agent/blob/main/Screenshot%202026-07-08%20172455.png)
* **Chat Interaction:**(https://github.com/iqrabatool1/ai-data-analyst-agent/blob/main/Screenshot%202026-07-08%20163216.png)
* **Chart Generation:** (https://github.com/iqrabatool1/ai-data-analyst-agent/blob/main/Screenshot%202026-07-08%20162745.png)

---

## ✨ Features

* **💬 Chat-based Interface:** Describe what you want in plain English and get results right in the conversation.
* **🔍 Filter & Analyze:** Handles complex syntax naturally, e.g., *"show only Punjab customers"*, *"average revenue by region"*, or *"which region has the highest revenue"*.
* **🧹 Permanent Cleaning (On Demand):** Supports actions like *"remove duplicates permanently"* or *"fill missing revenue with the average"*. The agent distinguishes between a temporary view and a permanent change, so casual questions never silently corrupt your data state.
* **📊 Visualizations:** Generates bar charts, pie charts, histograms, and scatter plots via Plotly straight from natural language.
* **🧪 Auto Data Quality Report:** The moment you upload a file, instantly see duplicate rows, missing values per column, and dtypes — zero AI tokens required.
* **↩️ Reset Button:** Instantly snap back to your original uploaded data at any time.
* **🔎 Transparent Code Generation:** Every AI-generated snippet is shown in an expander so you can see exactly what code ran under the hood.
* **🛡️ Sandboxed Execution:** Generated code is checked against a strict deny-list (blocking `import`, `exec`, `eval`, and file/OS access) before running.

---

## 🏗️ Architecture

```text
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
Keyword gate: Does the instruction actually ask for a PERMANENT change?
   ├── No  → Treated as a VIEW: displayed only, dataset unchanged
   └── Yes → Working dataset is updated permanently
     ↓
Result (table/chart) shown in chat + persisted across reruns
