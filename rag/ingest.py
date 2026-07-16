import os
from dotenv import load_dotenv
from openai import OpenAI

# Document loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)


from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings
from langchain_openai import OpenAIEmbeddings

# Vector store
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def build_vector_store():
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    docs = []

    # Load supported documents
    for file in os.listdir(upload_folder):
        path = os.path.join(upload_folder, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif file.endswith(".txt"):
            loader = TextLoader(path)
        elif file.endswith(".docx"):
            loader = Docx2txtLoader(path)
        else:
            continue

        loaded_docs = loader.load()

        # Add metadata for source file
        for doc in loaded_docs:
            doc.metadata["source_file"] = file

        docs.extend(loaded_docs)

    if not docs:
        raise ValueError("No supported documents found in uploads folder")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    # Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Build FAISS vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save locally
    os.makedirs("vector_store", exist_ok=True)
    vectorstore.save_local("vector_store")

    return len(chunks)
