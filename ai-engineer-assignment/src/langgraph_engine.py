# src/langgraph_engine.py
import re
from typing import Any, Dict, TypedDict
from langgraph.graph import StateGraph, END
from src.weather import get_weather_for_city, summarize_weather_payload
from src.rag_chain import build_rag_chain

# Weather keywords for classification
WEATHER_KEYWORDS = {"weather", "temperature", "rain", "forecast", "sunny", "wind", "windy", "snow", "cloud"}

class GraphState(TypedDict):
    """State for the LangGraph workflow"""
    query: str
    response: str
    city: str
    weather_data: Dict[str, Any]
    is_weather_query: bool
    rag_chain: Any
    llm: Any
    openweather_api_key: str

def looks_like_weather_query(text: str) -> bool:
    """Check if the query is about weather"""
    text_l = text.lower()
    return any(word in text_l for word in WEATHER_KEYWORDS)

def extract_city_from_query(text: str) -> str | None:
    """Extract city name from weather query"""
    # Very naive: look for 'in <city>' or 'at <city>'
    m = re.search(r"\b(?:in|at)\s+([A-Za-z\s\-]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # fallback: if query is single token or "weather <city>"
    m2 = re.search(r"weather\s+([A-Za-z\s\-]+)", text, re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return None

def decision_node(state: GraphState) -> GraphState:
    """Decision node that determines if query is about weather or should go to RAG"""
    query = state["query"]
    is_weather = looks_like_weather_query(query)
    
    return {
        **state,
        "is_weather_query": is_weather,
        "city": extract_city_from_query(query) or "your location" if is_weather else ""
    }

def weather_node(state: GraphState) -> GraphState:
    """Node that handles weather queries"""
    city = state["city"]
    api_key = state["openweather_api_key"]
    
    # Get weather data
    payload = get_weather_for_city(city, api_key=api_key)
    summary = summarize_weather_payload(payload)
    
    # Optionally enhance with LLM
    llm = state["llm"]
    if llm:
        try:
            prompt = f"Summarize the following weather for a user in one friendly sentence:\n\n{summary}"
            response = llm(prompt)
        except Exception:
            response = summary
    else:
        response = summary
    
    return {
        **state,
        "weather_data": payload,
        "response": response
    }

def rag_node(state: GraphState) -> GraphState:
    """Node that handles RAG queries"""
    query = state["query"]
    rag_chain = state["rag_chain"]
    
    try:
        # Try different ways to call the RAG chain
        if hasattr(rag_chain, 'run'):
            response = rag_chain.run(query)
        elif hasattr(rag_chain, 'invoke'):
            response = rag_chain.invoke({"query": query})
        else:
            response = f"Error: RAG chain doesn't have expected methods. Type: {type(rag_chain)}"
    except Exception as e:
        response = f"Error processing RAG query: {str(e)}"
    
    return {
        **state,
        "response": response
    }

def route_decision(state: GraphState) -> str:
    """Routing function that determines the next node based on query type"""
    if state["is_weather_query"]:
        return "weather"
    else:
        return "rag"

class LangGraphEngine:
    def __init__(self, rag_chain, llm, openweather_api_key: str | None = None):
        self.rag_chain = rag_chain
        self.llm = llm
        self.openweather_api_key = openweather_api_key
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        # Create the state graph
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("decision", decision_node)
        workflow.add_node("weather", weather_node)
        workflow.add_node("rag", rag_node)
        
        # Add conditional routing from decision node
        workflow.add_conditional_edges(
            "decision",
            route_decision,
            {
                "weather": "weather",
                "rag": "rag"
            }
        )
        
        # Add edges from processing nodes to end
        workflow.add_edge("weather", END)
        workflow.add_edge("rag", END)
        
        # Set entry point
        workflow.set_entry_point("decision")
        
        # Compile the graph
        return workflow.compile()
    
    def handle(self, query: str) -> str:
        """Handle a query using the LangGraph workflow"""
        # Initial state
        initial_state: GraphState = {
            "query": query,
            "response": "",
            "city": "",
            "weather_data": {},
            "is_weather_query": False,
            "rag_chain": self.rag_chain,
            "llm": self.llm,
            "openweather_api_key": self.openweather_api_key or ""
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return result["response"]
