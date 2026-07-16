# 🤖 AI-Powered Text-to-SQL + RAG Assistant

An intelligent data analytics assistant that combines **Text-to-SQL**, **Retrieval-Augmented Generation (RAG)**, and **Natural Language Querying** to enable users to interact with structured databases and unstructured documents using plain English.

## 🚀 Live Demo

🔗 https://rag-sql-cjbnuwmfmnpes6svg7mgwd.streamlit.app/

---

## 📌 Features

### 🗄️ Text-to-SQL
- Convert natural language questions into SQL queries.
- Execute generated SQL against a relational database.
- Display query results in tabular format.
- Automatically explain generated SQL queries.

### 📄 RAG-Based Document Question Answering
- Upload PDF documents.
- Automatically chunk and embed document content.
- Store embeddings in a vector database.
- Retrieve relevant context for user questions.
- Generate grounded answers from uploaded documents.

### 🔀 Hybrid Query Engine
- Automatically decides whether a question should be answered using:
  - Database queries
  - Document retrieval
  - Both (Hybrid Mode)

### 📊 AI Insights Generation
- Generate business insights from query results.
- Summarize trends and patterns.
- Provide natural language explanations.

### 🎨 Interactive Streamlit Interface
- Modern web-based UI.
- Query history tracking.
- SQL visibility toggle.
- Source document references.
- Real-time response generation.

---

## 🏗️ System Architecture

```text
User Query
     │
     ▼
 Hybrid Router
     │
 ┌───┴────────────┐
 │                │
 ▼                ▼
Text-to-SQL      RAG Pipeline
 │                │
 ▼                ▼
Database      Vector Store
 │                │
 └──────┬─────────┘
        ▼
  LLM Response
        ▼
 Streamlit UI
```

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- SQLAlchemy

### AI / LLM
- OpenAI GPT Models
- LangChain

### Retrieval
- FAISS Vector Store
- OpenAI Embeddings

### Document Processing
- PyPDF
- LangChain Text Splitters

### Database
- SQLite

---

## 📂 Project Structure

```text
rag-sql/
│
├── frontend.py                # Streamlit UI
├── hybrid.py                  # Hybrid query routing
├── main.py                    # SQL generation and execution
│
├── rag/
│   ├── ingest.py              # Document ingestion
│   ├── retriever.py           # Vector retrieval
│   └── vector_store.py        # FAISS management
│
├── amazon.db                  # Sample database
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-sql.git
cd rag-sql
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Run Application

```bash
streamlit run frontend.py
```

---

## 💬 Example Queries

### Database Questions

```text
Show top 10 selling products
```

```text
What is the total revenue generated last month?
```

```text
List customers who placed more than 5 orders
```

### Document Questions

```text
Summarize the uploaded PDF
```

```text
What are the key findings in the report?
```

```text
Explain the methodology section
```

### Hybrid Questions

```text
Compare sales data with insights from the uploaded business report
```

---

## 📈 Workflow

### Database Flow

```text
Natural Language
       │
       ▼
OpenAI GPT
       │
       ▼
SQL Query
       │
       ▼
Database Execution
       │
       ▼
Results + Insights
```

### RAG Flow

```text
PDF Upload
     │
     ▼
Chunking
     │
     ▼
Embedding Generation
     │
     ▼
FAISS Storage
     │
     ▼
Retrieval
     │
     ▼
Answer Generation
```

---

## 🎯 Key Highlights

- Natural Language to SQL Conversion
- Retrieval-Augmented Generation (RAG)
- PDF Question Answering
- Hybrid Database + Document Intelligence
- OpenAI GPT Integration
- FAISS Vector Search
- Streamlit Dashboard
- Real-Time Analytics

---

## 🔮 Future Improvements

- Multi-Database Support (MySQL, PostgreSQL)
- Chat History Memory
- User Authentication
- Query Optimization Layer
- CSV and Excel Upload Support
- Multi-Document Retrieval
- Source Citations
- Dashboard Visualizations

---

## 👩‍💻 Author

**Prachi Ahlawat**

B.Tech CSE (AI & ML)

Aspiring AI/LLM Engineer

---

## 📜 License

This project is licensed under the MIT License.