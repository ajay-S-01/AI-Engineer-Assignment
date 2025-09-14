from langchain.embeddings import HuggingFaceEmbeddings
from src.config import settings

def get_embeddings(model_name: str | None = None):
    model_name = model_name or settings.EMBEDDING_MODEL
    # Uses sentence-transformers under the hood
    return HuggingFaceEmbeddings(model_name=model_name)
