"""Pytest configuration and shared fixtures."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import Optional

# Add src to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# To this:
from src.config import Settings

@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    return Settings(
        OPENWEATHER_API_KEY="test_api_key",
        FAISS_INDEX_PATH="test_faiss_index",
        PDF_PATH="test_data/sample.pdf",
        EMBEDDING_MODEL="all-MiniLM-L6-v2",
        LLM_PROVIDER="gemini",
        GEMINI_API_KEY="test_gemini_key",
        GEMINI_MODEL="gemini-2.5-flash",
        OPENAI_API_KEY="test_openai_key",
        OPENAI_MODEL="gpt-4o-mini",
        LANGCHAIN_API_KEY="test_langchain_key"
    )

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_llm():
    """Mock LLM for testing."""
    mock_llm = Mock()
    mock_llm.return_value = "Mocked LLM response"
    return mock_llm

@pytest.fixture
def mock_rag_chain():
    """Mock RAG chain for testing."""
    mock_chain = Mock()
    mock_chain.run.return_value = "Mocked RAG response"
    return mock_chain

@pytest.fixture
def mock_vectorstore():
    """Mock vectorstore for testing."""
    mock_vs = Mock()
    mock_vs.as_retriever.return_value = Mock()
    return mock_vs

@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing."""
    return {
        "main": {
            "temp": 20.5,
            "feels_like": 22.0,
            "humidity": 65
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],
        "name": "London"
    }

@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    from langchain.schema import Document
    return [
        Document(
            page_content="This is a sample document about AI and machine learning.",
            metadata={"source": "test.pdf", "page": 1}
        ),
        Document(
            page_content="RAG stands for Retrieval-Augmented Generation.",
            metadata={"source": "test.pdf", "page": 2}
        )
    ]

# Pytest markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")