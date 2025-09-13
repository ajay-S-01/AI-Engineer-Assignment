"""AI Engineer Assignment - Weather and RAG Pipeline with LangGraph.

This package provides a comprehensive AI pipeline that combines:
- Weather information retrieval
- RAG (Retrieval-Augmented Generation) for document Q&A
- LangGraph for workflow orchestration
"""

__version__ = "0.1.0"
__author__ = "AI Engineer"
__email__ = "ai.engineer@example.com"

from .config import settings
from .langgraph_engine import LangGraphEngine
from .rag_chain import build_rag_chain
from .weather import get_weather_for_city, summarize_weather_payload
from .vectorstore import build_faiss_from_docs, load_faiss
from .embeddings import get_embeddings
from .llm_wrappers import get_llm

__all__ = [
    "settings",
    "LangGraphEngine", 
    "build_rag_chain",
    "get_weather_for_city",
    "summarize_weather_payload",
    "build_faiss_from_docs",
    "load_faiss",
    "get_embeddings",
    "get_llm",
]
