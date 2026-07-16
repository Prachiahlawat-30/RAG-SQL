from .main import generate_sql, execute_sql , answer_document_question
import pandas as pd


def hybrid_answer(question, db_path):

    # RAG Answer
    rag_result = answer_document_question(
        question
    )

    try:

        sql_query = generate_sql(
            question,
            db_path
        )

        columns, rows = execute_sql(
            sql_query,
            db_path
        )

        if rows:

            df = pd.DataFrame(
                rows,
                columns=columns
            )

            return {
                "type": "hybrid",
                "rag_answer": rag_result["answer"],
                "sources": rag_result["sources"],
                "sql": sql_query,
                "data": df
            }

    except Exception:
        pass

    return {
        "type": "rag",
        "rag_answer": rag_result["answer"],
        "sources": rag_result["sources"]
    }