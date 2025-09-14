from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import os
from pypdf.errors import EmptyFileError

def load_and_split_pdf(path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Load PDF and split into chunks suitable for embeddings/RAG.
    Returns list of langchain Document objects.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found at path: {path}")
    if os.path.getsize(path) == 0:
        raise EmptyFileError("Cannot read an empty file")

    loader = PyPDFLoader(path)
    try:
        docs = loader.load()
    except EmptyFileError as e:
        # Re-raise with a clearer message for the Streamlit UI
        raise EmptyFileError(f"PDF at '{path}' is empty or unreadable: {e}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = splitter.split_documents(docs)
    return split_docs
