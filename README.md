# Pro Data Agent — AI Data Analyst Agent

> **An autonomous AI agent that acts like a mini data analyst.** Upload a CSV, chat with it in plain English, and it filters, cleans, analyzes, and visualizes your data — powered by Google's Gemini API.

This is a "Digital FTE" style project: an AI agent that takes a specific user input, reasons about it, and performs a real automated task (not just chatting) — generating and safely executing pandas/Plotly code on real data.

🔗 **Live Demo:** [Add your Hugging Face Space / deployed link here]

---

## 📸 Demo

![App Screenshot](image.png)

*Placeholders for additional feature walkthroughs:*
* **Data Quality Report:** *[Insert screenshot/GIF here]*
* **Chat Interaction:** *[Insert screenshot/GIF here]*
* **Chart Generation:** *[Insert screenshot/GIF here]*

---

## 🚀 Features

* **💬 Chat-based Interface:** Describe what you want in plain English and get results directly within the conversation.
* **🔍 Filter & Analyze:** Handles queries like *"show only Punjab customers"*, *"average revenue by region"*, or *"which region has the highest revenue"*.
* **🧹 Permanent Cleaning (On Demand):** Supports commands like *"remove duplicates permanently"* or *"fill missing revenue with the average"*. The agent intelligently distinguishes between a temporary view and a permanent state change so casual questions never silently corrupt your data.
* **📊 Visualizations:** Generates bar charts, pie charts, histograms, and scatter plots via Plotly entirely from natural language.
* **🧪 Auto Data Quality Report:** The moment you upload a file, instantly see duplicate rows, missing values per column, and dtypes — zero AI calls or tokens required.
* **↩️ Reset Button:** Instantly snap back to your original uploaded data at any time.
* **🔎 Transparent Code Generation:** Every AI-generated snippet is displayed inside an expander so you can see exactly what code ran under the hood.
* **🛡️ Sandboxed Execution:** Generated code is verified against a strict deny-list (blocking `import`, `exec`, `eval`, and file/OS access) before execution.

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
Keyword gate: Does the instruction ask for a PERMANENT change?
   ├── No  → Treated as a VIEW: displayed only, dataset unchanged
   └── Yes → Working dataset is permanently updated
     ↓
Result (table/chart) shown in chat + persisted across reruns
