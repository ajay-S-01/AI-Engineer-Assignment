# LangGraph Workflow Structure

## Graph Flow

```
START → decision → [weather | rag] → END
```

## Node Details

### 1. Decision Node (`decision_node`)
- **Purpose**: Analyzes the query to determine if it's a weather query or RAG query
- **Input**: Query string
- **Output**: Updated state with `is_weather_query` flag and extracted city
- **Logic**: Uses keyword matching to classify query type

### 2. Weather Node (`weather_node`)
- **Purpose**: Handles weather-related queries
- **Input**: City name and API key
- **Output**: Weather data and formatted response
- **Logic**: 
  - Calls weather API
  - Summarizes weather data
  - Optionally enhances with LLM

### 3. RAG Node (`rag_node`)
- **Purpose**: Handles document-based queries
- **Input**: Query string and RAG chain
- **Output**: Response from document retrieval
- **Logic**: Uses RetrievalQA chain to answer questions

## Routing Logic

The `route_decision` function determines the next node:
- If `is_weather_query` is True → route to "weather"
- If `is_weather_query` is False → route to "rag"

## State Management

The `GraphState` TypedDict contains:
- `query`: Original user query
- `response`: Final response
- `city`: Extracted city name (for weather queries)
- `weather_data`: Raw weather API response
- `is_weather_query`: Boolean flag for routing
- `rag_chain`: RAG processing chain
- `llm`: Language model instance
- `openweather_api_key`: API key for weather service

## Key Improvements Over If-Else

1. **Modular Design**: Each processing step is a separate node
2. **Clear State Management**: All data flows through a well-defined state
3. **Extensible**: Easy to add new nodes or modify routing logic
4. **Debuggable**: Each node can be tested independently
5. **Visual Flow**: Clear understanding of data flow through the graph
