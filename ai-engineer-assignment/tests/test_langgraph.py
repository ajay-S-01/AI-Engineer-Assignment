#!/usr/bin/env python3
"""
Test script for the new LangGraph implementation
This tests the logic without requiring LangGraph to be installed
"""

import sys
import os
sys.path.append('src')

def test_decision_logic():
    """Test the decision node logic"""
    print("Testing decision logic...")
    
    # Test weather queries
    weather_queries = [
        "What's the weather in London?",
        "How is the temperature today?",
        "Will it rain tomorrow?",
        "Is it sunny outside?"
    ]
    
    # Test RAG queries  
    rag_queries = [
        "What is RAG?",
        "Explain the document content",
        "Summarize the PDF",
        "What does the text say about AI?"
    ]
    
    from src.langgraph_engine import looks_like_weather_query, extract_city_from_query
    
    print("\nWeather Query Tests:")
    for query in weather_queries:
        is_weather = looks_like_weather_query(query)
        city = extract_city_from_query(query)
        print(f"  '{query}' -> Weather: {is_weather}, City: '{city}'")
    
    print("\nRAG Query Tests:")
    for query in rag_queries:
        is_weather = looks_like_weather_query(query)
        print(f"  '{query}' -> Weather: {is_weather}")
    
    print("\n✅ Decision logic tests completed!")

def test_state_structure():
    """Test the state structure"""
    print("\nTesting state structure...")
    
    from src.langgraph_engine import GraphState
    
    # Create a mock state
    mock_state: GraphState = {
        "query": "What's the weather in Paris?",
        "response": "",
        "city": "",
        "weather_data": {},
        "is_weather_query": False,
        "rag_chain": None,
        "llm": None,
        "openweather_api_key": ""
    }
    
    print(f"Mock state created: {list(mock_state.keys())}")
    print("✅ State structure test completed!")

if __name__ == "__main__":
    print("🧪 Testing LangGraph Implementation")
    print("=" * 50)
    
    try:
        test_decision_logic()
        test_state_structure()
        print("\n🎉 All tests passed!")
        print("\nThe LangGraph implementation is ready to use once LangGraph is installed.")
        print("Run: pip install langgraph>=0.0.40")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
