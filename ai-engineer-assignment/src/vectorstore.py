# src/vectorstore.py
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
import os

def build_faiss_from_docs(docs: list[Document], embeddings: Embeddings, persist_path: str | None = None) -> FAISS:
    """
    Build and return FAISS index from docs.
    If persist_path is provided, save local files there.
    """
    vectorstore = FAISS.from_documents(docs, embeddings)
    if persist_path:
        os.makedirs(persist_path, exist_ok=True)
        vectorstore.save_local(persist_path)
    return vectorstore

def load_faiss(persist_path: str, embeddings: Embeddings) -> FAISS:
    """
    Load a previously saved FAISS index.
    """
    # LangChain >=0.1 may require explicit allow_dangerous_deserialization
    return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
