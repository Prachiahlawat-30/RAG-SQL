import os
import json
import re
import sqlite3
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI
from rag.retriever import retrieve

# ==================================================
# Load Environment Variables
# ==================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

# ==================================================
# Database Schema Extraction
# ==================================================

def extract_schema(db_path: str):

    engine = create_engine(f"sqlite:///{db_path}")

    inspector = inspect(engine)

    schema = {}

    for table in inspector.get_table_names():

        columns = inspector.get_columns(table)

        schema[table] = [
            column["name"]
            for column in columns
        ]

    return json.dumps(schema, indent=2)


# ==================================================
# SQL Cleaning
# ==================================================

def clean_sql(response: str):

    response = re.sub(
        r"<think>.*?</think>",
        "",
        response,
        flags=re.DOTALL,
    )

    response = response.replace("```sql", "")
    response = response.replace("```", "")

    return response.strip()


# ==================================================
# Text to SQL using OpenAI
# ==================================================

def generate_sql(user_query: str, db_path: str):

    schema = extract_schema(db_path)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert SQLite SQL generator.

Rules:
1. Return only SQL.
2. No explanation.
3. No markdown.
4. No reasoning.
5. Use ONLY tables and columns from the schema.
6. Generate valid SQLite SQL.
                """
            ),
            (
                "user",
                """
Schema:
{schema}

Question:
{query}

SQL:
                """
            )
        ]
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=OPENAI_API_KEY
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "schema": schema,
            "query": user_query
        }
    )

    return clean_sql(response.content)


# ==================================================
# Execute SQL
# ==================================================

def execute_sql(sql_query: str, db_path: str):

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute(sql_query)

    rows = cursor.fetchall()

    columns = []

    if cursor.description:
        columns = [
            column[0]
            for column in cursor.description
        ]

    conn.close()

    return columns, rows


# ==================================================
# Generate Business Insights
# ==================================================

def generate_insights(df: pd.DataFrame):

    if df.empty:
        return "No data available for analysis."

    data_sample = df.head(20).to_string()

    prompt = f"""
You are an expert business analyst.

Analyze the following dataset and provide:

1. Key Trends
2. Important Observations
3. Business Recommendations

Dataset:
{data_sample}

Keep the response concise and actionable.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "You are an expert business analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ==================================================
# Complete Query Pipeline
# ==================================================

def ask_database(question: str, db_path: str):

    print("\nGenerating SQL...\n")

    sql_query = generate_sql(
        user_query=question,
        db_path=db_path
    )

    print("Generated SQL:")
    print(sql_query)

    columns, rows = execute_sql(
        sql_query=sql_query,
        db_path=db_path
    )

    df = pd.DataFrame(rows, columns=columns)

    print("\nQuery Results:")
    print(df.head())

    insights = generate_insights(df)

    return {
        "sql": sql_query,
        "data": df,
        "insights": insights
    }


# ==================================================
# Example Usage
# ==================================================

if __name__ == "__main__":

    DB_PATH = "amazon.db"

    question = "What are the top 10 products with highest revenue?"

    result = ask_database(
        question=question,
        db_path=DB_PATH
    )

    print("\n" + "=" * 60)
    print("BUSINESS INSIGHTS")
    print("=" * 60)

    print(result["insights"])
    

def answer_document_question(question):

    docs = retrieve(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    sources = list(
        set(
            doc.metadata.get(
                "source_file",
                "Unknown"
            )
            for doc in docs
        )
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
    "role": "system",
    "content": """
You are a helpful AI research assistant.

Answer using only the retrieved context.

If the answer exists in the context:
- Explain clearly.
- Use simple language.
- Summarize if necessary.

If the answer is not in the context, say:
'I could not find this information in the uploaded documents.'
"""
},
            {
                "role": "user",
                "content":
                f"""
Context:
{context}

Question:
{question}
"""
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }