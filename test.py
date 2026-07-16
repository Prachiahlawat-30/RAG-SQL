from rag.ingest import build_vector_store

count = build_vector_store()

print(count)

from rag.retriever import retrieve

docs = retrieve(
    "What is an active customer?"
)

for doc in docs:
    print("\n------------------")
    print(doc.page_content)
    print(doc.metadata)
    

docs = retrieve("What is self attention?")

print(docs[0].page_content[:1000])