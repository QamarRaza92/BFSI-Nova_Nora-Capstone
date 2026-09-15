import os

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
POLICY_PATH = os.path.join(PROJECT_ROOT,"data","policies")
VECTOR_DB_PATH = os.path.join(PROJECT_ROOT,"data","faiss_index")

# 1. Load policy PDFs
def load_pdf_files(data_path):
    loader = DirectoryLoader(
        data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    if not documents:
        raise ValueError("No PDF files found in data/policies/")
    else:
        return documents


# 2. Add policy metadata
def add_policy_metadata(documents):
    for document in documents:
        source = document.metadata.get("source", "")
        filename = os.path.basename(source)
        policy_id = (filename.replace("policy_", "").replace(".pdf", ""))

        document.metadata["policy_id"] = policy_id

    return documents


# 3. Create chunks
def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No text chunks were generated from the PDFs.")
    else:
        return chunks


# 4. Create local embedding model
def create_embedding_model():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model


# 5. Build and save FAISS database
def build_vector_database(chunks, embedding_model):
    vector_db = FAISS.from_documents(documents=chunks,embedding=embedding_model)
    vector_db.save_local(VECTOR_DB_PATH)
    return vector_db

# Run the file
if __name__ == "__main__":
    print("Loading policy PDFs...")
    documents = load_pdf_files(POLICY_PATH)
    print(f"Loaded {len(documents)} PDF pages.")
    documents = add_policy_metadata(documents)
    print("Policy metadata added.")

    chunks = create_chunks(documents)
    print(f"Created {len(chunks)} chunks.")
    print("Loading local HuggingFace embedding model...")
    embedding_model = create_embedding_model()

    print("Creating FAISS vector database...")
    vector_db = build_vector_database(
        chunks,
        embedding_model
    )

    print("\nFAISS database created successfully!")
    print(f"Saved at: {VECTOR_DB_PATH}")

















# import os
# from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
# from langchain_core.prompts import PromptTemplate
# from langchain_text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma, FAISS
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings


# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# GROQ_MODEL_ID = "openai/gpt-oss-20b"


# DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "policies")
# print("Hi there: ",DATA_PATH)


# def load_pdf_files(data):
#     loader = DirectoryLoader(data,
#                              glob="*.pdf",
#                              loader_cls=PyPDFLoader)
#     documents = loader.load()
#     return documents

# # Load global document vectors locally
# raw_documents = load_pdf_files(data=DATA_PATH)

# # Using local SentenceTransformer for embedding parsing calculations
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# def build_configurable_knowledge_base(documents, chunk_size, chunk_overlap):
#     """Dynamically slices and rebuilds a FAISS database array for parameter tuning."""
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     # Uses split_documents directly on your loader output
#     text_chunks = text_splitter.split_documents(documents)
    
#     # Simple safety barrier if document extraction fails to load text
#     if not text_chunks:
#         raise ValueError("No text chunks generated. Ensure your PDF has selectable text and is in the 'data/' folder.")
        
#     db = FAISS.from_documents(text_chunks, embedding_model)
#     return db



# def load_chat_llm():
#     """Initializes the stable Groq API cloud connection footprint."""
#     if not GROQ_API_KEY:
#         raise ValueError("GROQ_API_KEY not found.")
    
#     return ChatGroq(
#         model=GROQ_MODEL_ID,
#         temperature=0.1, # Low temperature for consistent grading evaluations
#         groq_api_key=GROQ_API_KEY
#     )

# CUSTOM_PROMPT_TEMPLATE = """Use the pieces of information provided in the context to answer user's question.
# If you dont know the answer, just say that you dont know, dont try to make up an answer. 
# Dont provide anything out of the given context

# Context: {context}
# Question: {input}

# Start the answer directly. No small talk please."""

# prompt_template = PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "input"])
# chat_llm = load_chat_llm()