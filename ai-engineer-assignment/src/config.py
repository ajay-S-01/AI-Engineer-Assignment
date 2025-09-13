# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str | None = None
    FAISS_INDEX_PATH: str = "faiss_index"
    PDF_PATH: str = "data/sample.pdf"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # LLM provider
    LLM_PROVIDER: str = "gemini"  # "gemini" or "openai"

    # Gemini (API key)
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # LangSmith
    LANGSMITH_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()