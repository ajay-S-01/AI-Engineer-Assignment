import pytest
import sys
import os

# Ensure src is on path
sys.path.append("src")


def test_weather_query_detection():
    """Test detection of weather queries"""
    from src.langgraph_engine import looks_like_weather_query, extract_city_from_query

    queries = [
        ("What's the weather in London?", True, "London"),
        ("How is the temperature today?", True, None),
        ("Will it rain tomorrow?", True, None),
        ("Is it sunny outside?", True, None),
    ]

    for query, expected_weather, expected_city in queries:
        assert looks_like_weather_query(query) == expected_weather
        assert extract_city_from_query(query) == expected_city


def test_rag_query_detection():
    """Test detection of non-weather (RAG) queries"""
    from src.langgraph_engine import looks_like_weather_query

    queries = [
        "What is RAG?",
        "Explain the document content",
        "Summarize the PDF",
        "What does the text say about AI?",
    ]

    for query in queries:
        assert not looks_like_weather_query(query)


def test_state_structure():
    """Ensure GraphState structure matches expected keys"""
    from src.langgraph_engine import GraphState

    mock_state: GraphState = {
        "query": "What's the weather in Paris?",
        "response": "",
        "city": "",
        "weather_data": {},
        "is_weather_query": False,
        "rag_chain": None,
        "llm": None,
        "openweather_api_key": "",
    }

    expected_keys = {
        "query",
        "response",
        "city",
        "weather_data",
        "is_weather_query",
        "rag_chain",
        "llm",
        "openweather_api_key",
    }
    assert set(mock_state.keys()) == expected_keys
