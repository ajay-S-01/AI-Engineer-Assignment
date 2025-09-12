# src/langgraph_engine.py
import re
from typing import Any
from src.weather import get_weather_for_city, summarize_weather_payload
from src.rag_chain import build_rag_chain

# Simple rule-based "decision node" that acts like a tiny LangGraph
WEATHER_KEYWORDS = {"weather", "temperature", "rain", "forecast", "sunny", "wind", "windy", "snow", "cloud"}

def looks_like_weather_query(text: str) -> bool:
    text_l = text.lower()
    return any(word in text_l for word in WEATHER_KEYWORDS)

def extract_city_from_query(text: str) -> str | None:
    # Very naive: look for 'in <city>' or 'at <city>'
    m = re.search(r"\b(?:in|at)\s+([A-Za-z\s\-]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # fallback: if query is single token or "weather <city>"
    m2 = re.search(r"weather\s+([A-Za-z\s\-]+)", text, re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return None

class LangGraphEngine:
    def __init__(self, rag_chain, llm, openweather_api_key: str | None = None):
        self.rag_chain = rag_chain
        self.llm = llm
        self.openweather_api_key = openweather_api_key

    def handle(self, query: str) -> str:
        if looks_like_weather_query(query):
            city = extract_city_from_query(query) or "your location"
            payload = get_weather_for_city(city, api_key=self.openweather_api_key)
            summary = summarize_weather_payload(payload)
            # Optionally call LLM to rephrase / expand
            try:
                prompt = f"Summarize the following weather for a user in one friendly sentence:\n\n{summary}"
                llm_resp = self.llm(prompt)
                return llm_resp
            except Exception:
                return summary
        else:
            # Default to RAG answering
            return self.rag_chain.run(query)
