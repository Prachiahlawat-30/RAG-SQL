🤖 RAGSQL – AI Data Analytics Assistant
An AI-powered Hybrid Data Analytics Assistant that allows users to interact with databases and enterprise documentation using natural language. Instead of writing SQL queries manually, users can simply ask questions in plain English, and the system automatically generates SQL, retrieves relevant context using RAG (Retrieval-Augmented Generation), applies business rules, executes queries, visualizes results, and provides actionable insights.

📌 Project Overview
RAGSQL is a Streamlit-based web application that combines:

Text-to-SQL for structured database querying

RAG (Retrieval-Augmented Generation) for contextual answers from enterprise docs

Hybrid AI querying that blends structured + unstructured data sources

Business-rule-aware analytics to ensure compliance and domain-specific logic

Interactive visualization for instant insights

This makes it ideal for analysts, researchers, students, and business users who want powerful analytics without needing SQL or deep technical expertise.

🚀 Features
🔹 Natural Language to SQL
Convert user questions into optimized SQL queries automatically using LLMs.

Example:

Code
User Input:
Show top 5 customers by total sales

Generated SQL:
SELECT customer_name, SUM(amount)
FROM orders
GROUP BY customer_name
ORDER BY SUM(amount) DESC
LIMIT 5;
🔹 RAG-Powered Contextual Insights
Retrieves relevant documentation, manuals, or enterprise knowledge base entries.

Answers questions that require both data + context.

Example: “What were the top 3 products last quarter, and what business rules apply to their pricing?”

🔹 Hybrid AI Querying
Combines structured SQL results with unstructured text retrieval.

Enables analytics across databases + documents simultaneously.

Example: “Summarize customer churn trends and include related policy notes.”

🔹 Business-Rule-Aware Querying
Queries respect compliance, governance, and organizational rules.

Prevents invalid or non-compliant queries.

Example: “Show sales excluding restricted regions.”

🔹 Interactive Data Visualization
Automatically generates charts from query results:

Bar Charts

Pie Charts

Line Charts

Scatter Plots

Histograms

🔹 AI-Powered Insights
Analyzes query results and generates business insights such as:

Trends

Patterns

Outliers

Recommendations

🔹 Query History & Export
Stores conversation history using Streamlit Session State.

Export query results as CSV.

🔹 Dynamic Schema + Knowledge Explorer
Displays database tables, columns, and structure.

Shows available enterprise documents for RAG queries.

🛠️ Tech Stack
Frontend: Streamlit

Backend: Python

Database: SQLite (future: MySQL, PostgreSQL, SQL Server)

AI Models: Ollama (Llama 3, Qwen2.5), Hybrid RAG pipeline

Data Processing: Pandas

Visualization: Plotly Express

Database Inspection: SQLAlchemy

📊 Workflow
User uploads SQLite database.

Database schema + enterprise docs are extracted.

User enters natural language query.

AI converts text into SQL + retrieves context with RAG.

SQL executes on database.

Results + retrieved docs are merged.

Charts + insights are generated.

Business rules applied.

Results displayed + export option.

🏗️ System Architecture
Code
User
↓
Streamlit UI
↓
Natural Language Query
↓
LLM (Text-to-SQL + RAG)
↓
Business Rules Engine
↓
SQLite Database + Docs
↓
Query Execution + Retrieval
↓
Pandas DataFrame
↓
Charts + Insights
↓
Results Display
📈 Sample Queries
Show top 5 customers by sales

Summarize revenue trends and include compliance notes

Show monthly sales trend with related documentation

Find repeat customers and attach policy references

Show top products and explain pricing rules

🎯 Use Cases
Business Analytics: Sales, revenue, customer insights

Education: SQL learning + hybrid AI exploration

Research: Data + document-driven analysis

Decision Support: Trend detection, compliance-aware insights

🔮 Future Enhancements
Multi-database support (MySQL, PostgreSQL, SQL Server)

Dashboard builder

PDF/Report generation

Voice-based queries

Authentication system

Real-time analytics

Multi-user support

👨‍💻 Author
Prachi Ahlawat
B.Tech CSE (AI & ML)
RAGSQL – Hybrid AI Data Analytics Assistant

⭐ Acknowledgements
Streamlit

Pandas

Plotly

SQLAlchemy

SQLite

Ollama

Llama 3 / Qwen2.5

Python Community