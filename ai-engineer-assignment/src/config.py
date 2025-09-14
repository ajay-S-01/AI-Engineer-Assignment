# src/config.py
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

class Settings(BaseSettings):
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str = "ai-engineer-assignment"
    LANGCHAIN_API_KEY: Optional[str] = None

    OPENWEATHER_API_KEY: Optional[str] = None
    FAISS_INDEX_PATH: str = "faiss_index"
    PDF_PATH: str = "data/sample.pdf"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # LLM provider
    LLM_PROVIDER: str = "gemini"  # "gemini" or "openai"

    # Gemini (API key)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = Settings()