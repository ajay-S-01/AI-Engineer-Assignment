# src/llm_wrappers.py
from src.config import settings

# OpenAI imports
from langchain.chat_models import ChatOpenAI

# Gemini imports (API key version)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None


def get_llm():
    """
    Returns an LLM instance (Gemini or OpenAI), based on LLM_PROVIDER in config.
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        if not ChatGoogleGenerativeAI:
            raise ImportError(
                "Gemini support requires: pip install langchain-google-genai google-generativeai"
            )
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0,
        )

    elif provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}. Use 'gemini' or 'openai'."
        )
