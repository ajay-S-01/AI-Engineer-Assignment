# src/data_loader.py
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

def load_and_split_pdf(path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Load PDF and split into chunks suitable for embeddings/RAG.
    Returns list of langchain Document objects.
    """
    loader = PyPDFLoader(path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = splitter.split_documents(docs)
    return split_docs
