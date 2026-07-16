import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)


def classify_question(question):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
Classify the question into one category:

SQL
RAG
HYBRID

Examples:

Show all customers -> SQL

Top 5 products -> SQL

What is self attention -> RAG

Explain customer churn -> RAG

How many active customers do we have -> HYBRID

Return only one word.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
        .upper()
    )