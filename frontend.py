
import streamlit as st
import pandas as pd
import tempfile
import os
import json
from datetime import datetime
from sqlalchemy import create_engine, inspect
from hybrid import hybrid_answer
from main import generate_sql, execute_sql, generate_insights, answer_document_question
from rag.ingest import build_vector_store

# ==========================================
# QUERY HISTORY SETUP
# ==========================================

HISTORY_FILE = "history/query_history.json"
os.makedirs("history", exist_ok=True)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

st.set_page_config(
    page_title="AI Data Analytics Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state defaults
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "df" not in st.session_state:
    st.session_state.df = None
if "sql_query" not in st.session_state:
    st.session_state.sql_query = None
if "insights" not in st.session_state:
    st.session_state.insights = ""
if "selected_query" not in st.session_state:
    st.session_state.selected_query = None
if "mode" not in st.session_state:
    st.session_state.mode = "SQL Analytics"

table_count = 0
db_path = "amazon.db"

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("---")
    st.subheader("🎯 AI Mode")

    st.session_state.mode = st.radio(
        "Choose Assistant",
        ["SQL Analytics", "Knowledge Base", "Hybrid AI"]
    )

    st.title("📂 Database")
    uploaded_db = st.file_uploader("Upload SQLite Database", type=["db", "sqlite", "sqlite3"])
    if uploaded_db is not None:
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        temp_db.write(uploaded_db.read())
        temp_db.close()
        db_path = temp_db.name
        st.success(f"Loaded: {uploaded_db.name}")

    st.markdown("---")
    st.subheader("📚 Knowledge Base")

    uploaded_docs = st.file_uploader("Upload Documents", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    os.makedirs("uploads", exist_ok=True)

    if uploaded_docs:
        for doc in uploaded_docs:
            with open(os.path.join("uploads", doc.name), "wb") as f:
                f.write(doc.getbuffer())
        st.success(f"{len(uploaded_docs)} document(s) uploaded")

    if st.button("🔄 Build Knowledge Base"):
        try:
            chunk_count = build_vector_store()
            st.success(f"Knowledge Base built successfully ({chunk_count} chunks)")
        except Exception as e:
            st.error(str(e))

    st.markdown("---")
    st.metric("OpenAI", "Connected" if os.getenv("OPENAI_API_KEY") else "Missing")

    st.markdown("---")
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.df = None
        st.session_state.insights = ""
        st.rerun()

    st.markdown("---")
    st.subheader("🕒 Query History")
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    for item in reversed(history[-10:]):
        if st.button(item["question"], key=item["timestamp"]):
            st.session_state.selected_query = item["question"]

    st.markdown("---")
    try:
        engine = create_engine(f"sqlite:///{db_path}")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        table_count = len(tables)

        st.subheader("📊 Tables")
        for table in tables:
            with st.expander(table):
                for col in inspector.get_columns(table):
                    st.write(f"• {col['name']}")
    except Exception:
        st.warning("Database not found")

    st.markdown("---")
    st.subheader("💡 Example Queries")
    st.caption("Show all customers")
    st.caption("Show top 5 orders")
    st.caption("Sales by category")
    st.caption("Top products by revenue")

# ==========================================
# MAIN PAGE
# ==========================================
st.markdown("# 🤖 RAGSQL <br> (Retrieval-Augmented Generation + SQL fusion)", unsafe_allow_html=True)

record_count = len(st.session_state.df) if st.session_state.df is not None else 0
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Tables", table_count)
with c2: st.metric("Records", record_count)
with c3: st.metric("Database", "SQLite")
with c4: st.metric("AI", "GPT-4o Mini")

st.markdown("### 🚀 Quick Start")
col1, col2, col3 = st.columns(3)
prompt = None
if col1.button("👥 Show Customers"): prompt = "Show all customers"
if col2.button("💰 Top Orders"): prompt = "Show top 5 highest orders"
if col3.button("📦 Sales By Category"): prompt = "Show sales by category"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# CHAT INPUT
# ==========================================
placeholder = "Ask anything about your database..." if st.session_state.mode == "SQL Analytics" else "Ask anything about your documents..."
user_prompt = st.chat_input(placeholder)

if st.session_state.selected_query:
    prompt = st.session_state.selected_query
    st.session_state.selected_query = None
elif user_prompt:
    prompt = user_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if st.session_state.mode == "Knowledge Base":
                with st.spinner("Searching documents..."):
                    result = answer_document_question(prompt)
                st.markdown(result["answer"])
                st.markdown("### Sources")
                for source in result["sources"]:
                    st.info(f"📄 {source}")
                st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

            elif st.session_state.mode == "Hybrid AI":
                with st.spinner("Thinking..."):
                    result = hybrid_answer(prompt, db_path)
                st.markdown("## 🤖 Hybrid AI Answer")
                st.markdown(result["rag_answer"])

                if "sql" in result:
                    st.markdown("### Generated SQL")
                    st.code(result["sql"], language="sql")

                if "data" in result:
                    st.markdown("### Database Results")
                    st.dataframe(result["data"], width="stretch")

                st.markdown("### Sources")
                for source in result["sources"]:
                    st.info(f"📄 {source}")

                st.session_state.messages.append({"role": "assistant", "content": result["rag_answer"]})

            else:  # SQL Analytics
                with st.spinner("Generating SQL..."):
                    sql_query = generate_sql(prompt, db_path)

                with open(HISTORY_FILE, "r") as f:
                    history = json.load(f)
                history.append({"question": prompt, "sql": sql_query, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                with open(HISTORY_FILE, "w") as f:
                    json.dump(history, f, indent=4)

                st.code(sql_query, language="sql")
                columns, rows = execute_sql(sql_query, db_path)

                if rows:
                    df = pd.DataFrame(rows, columns=columns)
                    st.session_state.df = df
                    st.session_state.sql_query = sql_query
                    st.success(f"Found {len(df)} records")
                else:
                    st.session_state.df = None
                    st.info("No records found")

                st.session_state.messages.append({"role": "assistant", "content": f"```sql\n{sql_query}\n```"})

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==========================================
# RESULTS TABS
# ==========================================
if st.session_state.df is not None:
    df = st.session_state.df
    tab1, tab3, tab4 = st.tabs(

        ["📊 Results",  "🤖 Insights", "Knowledge Base"]

    )

    with tab1:
        st.dataframe(
            df,
            width="stretch",
            hide_index=True

        )
        csv = df.to_csv(index=False)
        st.download_button(

            "⬇ Download CSV",
            csv,
            "results.csv",
            "text/csv"
        )
    

    with tab3:

        summary = f"""

Total Rows: {len(df)}



Total Columns: {len(df.columns)}

"""



        numeric_df = df.select_dtypes(

            include=["number"]

        )



        if not numeric_df.empty:



            highest = numeric_df.max().max()

            lowest = numeric_df.min().min()



            summary += f"""

Highest Value: {highest}

Lowest Value: {lowest}

"""
        st.info(summary)
        st.subheader("🤖 AI Insights")
        if st.button(

            "Generate Insights",

            key="generate_ai_insights"

        ):
            with st.spinner("Analyzing data..."):
                st.session_state.insights = generate_insights(df)

        if st.session_state.insights:
            st.markdown(st.session_state.insights)

        with tab4:

            question = st.text_input(
                "Ask your documents"
            )

            if st.button("Ask Knowledge Base"):

                if question:

                    st.session_state.answer = (

                        answer_document_question(question)

                    )
            if "answer" in st.session_state:

                st.markdown("### Answer")
                st.markdown(
                    st.session_state.answer["answer"]
                )
                st.markdown("### Sources")

                for source in st.session_state.answer["sources"]:

                    st.info(f"📄 {source}")