import re

import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types

st.set_page_config(page_title="Pro Data Agent", layout="wide")
st.title("Pro Data Agent - Persistent Workspace")

# ----------------------------------------------------------------------------
# 1. Initialize State
# ----------------------------------------------------------------------------
if "projects" not in st.session_state:
    st.session_state.projects = {}

# ----------------------------------------------------------------------------
# 2. Sidebar: Project Management
# ----------------------------------------------------------------------------
st.sidebar.header("Project Management")
uploaded_file = st.sidebar.file_uploader("Upload New CSV", type=["csv"])

if uploaded_file:
    file_name = uploaded_file.name
    if file_name not in st.session_state.projects:
        df = pd.read_csv(uploaded_file)
        st.session_state.projects[file_name] = {
            "df": df,
            "original_df": df.copy(),  # <-- never touched after upload, used for reset
            "messages": [],
        }
    st.session_state.current_project = file_name

# Project Selection & Row Viewer
if st.session_state.projects:
    selected_project = st.sidebar.selectbox("Select Project", list(st.session_state.projects.keys()))
    st.session_state.current_project = selected_project
    num_rows = st.sidebar.slider("Rows to preview", 5, 50, 10)
    if st.sidebar.button("🔄 Reset to original uploaded data"):
        proj = st.session_state.projects[selected_project]
        proj["df"] = proj["original_df"].copy()
        st.sidebar.success("Reset done. Your original data is back.")

api_key = st.sidebar.text_input("Gemini API Key", type="password")
model_name = st.sidebar.selectbox(
    "Model",
    ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-3.5-flash", "gemini-2.5-pro"],
    index=0,
    help="If you get a 'model not found' error, Google may have retired it — check "
         "https://ai.google.dev/gemini-api/docs/models for the current list.",
)

# ----------------------------------------------------------------------------
# Safety: restrict what the generated code is allowed to do
# ----------------------------------------------------------------------------
FORBIDDEN_PATTERNS = [
    r"\bimport\b", r"\bopen\b", r"\bexec\b", r"\beval\b", r"__",
    r"\bos\.", r"\bsys\.", r"\bsubprocess\b", r"\bshutil\b",
    r"\bglobals\b", r"\blocals\b", r"\bcompile\b", r"\binput\b", r"\bdel\b",
]

# Only these keywords in the USER'S instruction unlock a permanent change to
# the working dataset. This is enforced in code (not just asked of the model)
# because the model doesn't always follow the result_df/view_df instruction
# perfectly. Everything else — filters, "show only", analysis — stays a view.
CLEANING_KEYWORDS = [
    "duplicate", "missing", "null", "clean", "permanent", "fill", "impute",
    "drop column", "delete column", "remove column", "dedupe", "de-dupe",
    "standardize", "correct", "fix typo", "rename column",
]


def instruction_allows_permanent_change(instruction: str) -> bool:
    text = instruction.lower()
    return any(keyword in text for keyword in CLEANING_KEYWORDS)


def is_code_safe(code: str) -> bool:
    return not any(re.search(pattern, code) for pattern in FORBIDDEN_PATTERNS)


def run_generated_code(code: str, df: pd.DataFrame):
    """Execute generated code in a restricted namespace.
    Returns (result_df, view_df, fig):
      - result_df: a transformation that should REPLACE the working dataset
      - view_df:   an analysis/query result to DISPLAY only (dataset unchanged)
      - fig:       a plotly figure to display
    """
    if not is_code_safe(code):
        raise ValueError("Generated code contained a disallowed operation and was blocked.")

    safe_builtins = {
        "len": len, "range": range, "sum": sum, "min": min, "max": max,
        "sorted": sorted, "abs": abs, "round": round, "list": list, "dict": dict,
        "str": str, "int": int, "float": float, "bool": bool, "True": True, "False": False,
    }
    local_vars = {"df": df.copy(), "pd": pd, "px": px}
    exec(code, {"__builtins__": safe_builtins}, local_vars)  # noqa: S102 - sandboxed above

    result_df = local_vars.get("result_df")
    view_df = local_vars.get("view_df")
    fig = local_vars.get("fig")

    # Fallback: if the model forgot the exact variable name, look for any
    # other DataFrame/Series it created and treat it as a view (safe default).
    if result_df is None and view_df is None and fig is None:
        for name, value in local_vars.items():
            if name in ("df", "pd", "px"):
                continue
            if isinstance(value, (pd.DataFrame, pd.Series)):
                view_df = value
                break

    return result_df, view_df, fig


def build_data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Pure-pandas data quality profile — no AI call needed, instant and free."""
    n_rows = len(df)
    rows = []
    for col in df.columns:
        series = df[col]
        null_count = int(series.isnull().sum())
        rows.append({
            "column": col,
            "dtype": str(series.dtype),
            "nulls": null_count,
            "null_%": round(100 * null_count / n_rows, 1) if n_rows else 0.0,
            "unique_values": int(series.nunique()),
        })
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# 3. Main Logic
# ----------------------------------------------------------------------------
if "current_project" in st.session_state and st.session_state.current_project:
    proj = st.session_state.projects[st.session_state.current_project]

    st.subheader(f"Working on: {st.session_state.current_project}")
    st.dataframe(proj["df"].head(num_rows))

    # --- Auto Data Quality Report (computed instantly, no AI call) ---
    with st.expander("📊 Data Quality Report", expanded=True):
        current_df = proj["df"]
        dup_count = int(current_df.duplicated().sum())
        total_nulls = int(current_df.isnull().sum().sum())

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows", len(current_df))
        m2.metric("Columns", len(current_df.columns))
        m3.metric("Duplicate rows", dup_count)
        m4.metric("Total missing values", total_nulls)

        st.dataframe(build_data_quality_report(current_df), use_container_width=True)

        if dup_count > 0 or total_nulls > 0:
            st.caption(
                "💡 Try asking the chat: *'remove duplicates permanently'* or "
                "*'fill missing values with the average, permanently'*."
            )
        else:
            st.caption("✅ No duplicates or missing values detected.")

    # Download Button
    csv = proj["df"].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Current Data",
        csv,
        f"processed_{st.session_state.current_project}",
        "text/csv",
    )

    # Display History (now re-renders charts too, using a stored fig per message)
    for i, msg in enumerate(proj["messages"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "table" in msg:
                st.dataframe(msg["table"], use_container_width=True)
            if "fig" in msg:
                st.plotly_chart(msg["fig"], key=f"chart_{st.session_state.current_project}_{i}")

    # Chat Interaction
    if prompt := st.chat_input("Ask me to analyze, clean, or visualize..."):
        proj["messages"].append({"role": "user", "content": prompt})
        st.rerun()

    # Process if last message is from user (prevents infinite loops)
    if proj["messages"] and proj["messages"][-1]["role"] == "user":
        with st.chat_message("assistant"):
            if not api_key:
                st.error("Please enter your Gemini API Key in the sidebar.")
            else:
                try:
                    client = genai.Client(api_key=api_key)
                    context = f"Columns: {proj['df'].columns.tolist()}"

                    response = client.models.generate_content(
                        model=model_name,
                        contents=(
                            f"Context: {context}. Task: {proj['messages'][-1]['content']}. "
                            f"Save result to 'result_df' or 'fig'."
                        ),
                        config=types.GenerateContentConfig(
                            system_instruction=(
                                "You are a silent analyst. Output ONLY Python code using pandas "
                                "(as pd) and plotly.express (as px) on the existing dataframe `df`. "
                                "Do not import anything, do not read/write files, do not use exec/eval. "
                                "No backticks, no comments, no headers — code only.\n\n"
                                "IMPORTANT — choose the right output variable:\n"
                                "- Assign your answer to `view_df` for almost everything: filtering "
                                "(e.g. 'show rows where revenue > 5000', 'only Punjab customers'), "
                                "sorting, and analysis/aggregation (averages, counts, totals, "
                                "'which region is highest'). These are TEMPORARY VIEWS — the "
                                "underlying dataset is NOT changed, so the user can keep asking "
                                "questions against the full original data afterward.\n"
                                "- Only assign to `result_df` when the user explicitly asks to "
                                "PERMANENTLY clean or modify the stored data itself — e.g. 'remove "
                                "duplicates', 'fill missing values', 'drop the email column', 'delete "
                                "rows with nulls permanently'. This replaces the working dataset for "
                                "all future questions, so use it sparingly and only for genuine "
                                "cleaning requests.\n"
                                "- If asked to make a chart, assign it to `fig`.\n"
                                "- ALWAYS assign your final answer to one of these three exact names: "
                                "`view_df`, `result_df`, or `fig`. Never leave the answer in a "
                                "differently-named variable."
                            )
                        ),
                    )

                    code = response.text.strip().replace("```", "").replace("python", "")

                    with st.expander("🔍 Generated code (transparency)"):
                        st.code(code, language="python")

                    result_df, view_df, fig = run_generated_code(code, proj["df"])
                    user_instruction = proj["messages"][-1]["content"]

                    assistant_msg = {"role": "assistant", "content": ""}

                    if fig is not None:
                        st.plotly_chart(fig, key=f"chart_new_{len(proj['messages'])}")
                        assistant_msg["content"] = "Chart generated."
                        assistant_msg["fig"] = fig  # <-- persist the figure so it survives rerun

                    if view_df is not None:
                        # Analysis/filter result: DISPLAY only, do NOT touch proj["df"]
                        st.dataframe(view_df, use_container_width=True)
                        assistant_msg["content"] = (
                            assistant_msg["content"] + " Here's the result (view only — your full "
                            "dataset is unchanged)."
                        ).strip()
                        assistant_msg["table"] = view_df  # persist so it re-renders after rerun

                    if result_df is not None:
                        if instruction_allows_permanent_change(user_instruction):
                            # Cleaning: this PERMANENTLY REPLACES the working dataset going forward
                            proj["df"] = result_df
                            st.dataframe(result_df, use_container_width=True)
                            assistant_msg["content"] = (
                                assistant_msg["content"] + " Your working dataset has been "
                                "permanently updated."
                            ).strip()
                            assistant_msg["table"] = result_df
                        else:
                            # The model produced result_df, but the instruction didn't ask for a
                            # permanent change — downgrade it to a view for safety.
                            st.dataframe(result_df, use_container_width=True)
                            assistant_msg["content"] = (
                                assistant_msg["content"] + " Here's the result (view only — your "
                                "full dataset is unchanged). Say something like 'remove duplicates "
                                "permanently' if you actually want this saved."
                            ).strip()
                            assistant_msg["table"] = result_df

                    if not assistant_msg["content"]:
                        assistant_msg["content"] = (
                            "I ran the code but it didn't produce `result_df`, `view_df`, or `fig`. "
                            "Try rephrasing your request."
                        )

                    proj["messages"].append(assistant_msg)
                    st.rerun()

                except Exception as e:
                    st.error(f"Execution failed: {e}")
else:
    st.info("Upload a CSV in the sidebar to get started.")