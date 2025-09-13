# AI Engineer Assignment

A comprehensive AI pipeline that combines weather information retrieval and RAG (Retrieval-Augmented Generation) capabilities using LangGraph for workflow orchestration.

## Features

- 🌤️ **Weather Integration**: Get real-time weather information for any city
- 📚 **RAG Pipeline**: Ask questions about uploaded PDF documents
- 🔄 **LangGraph Workflow**: Intelligent routing between weather and RAG based on query type
- 🎯 **Multiple UIs**: Streamlit app, React frontend, and FastAPI backend
- 🔧 **Modular Design**: Clean, extensible architecture
- 🐳 **Docker Ready**: Easy deployment with Docker Compose
- 🚀 **Production Ready**: FastAPI backend with CORS, React frontend with TypeScript

## Architecture

The system uses LangGraph to create a workflow that intelligently routes queries:

```
START → Decision Node → [Weather Node | RAG Node] → END
```

- **Decision Node**: Analyzes queries to determine if they're weather-related or document-related
- **Weather Node**: Handles weather queries using OpenWeather API
- **RAG Node**: Processes document questions using retrieval-augmented generation

## Installation

### Prerequisites

- Python 3.8+
- pip or poetry

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-engineer-assignment
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   # or for development
   pip install -e ".[dev]"
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Required API Keys**
   - OpenWeather API key (for weather functionality)
   - Gemini API key OR OpenAI API key (for LLM functionality)

## Configuration

Create a `.env` file with the following variables:

```env
# Weather API
OPENWEATHER_API_KEY=your_openweather_api_key_here

# LLM Configuration
LLM_PROVIDER=gemini  # Options: "gemini" or "openai"

# Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# File Paths
PDF_PATH=data/sample.pdf
FAISS_INDEX_PATH=faiss_index

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Usage

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Development Mode

#### Start Backend and Frontend Together
```bash
# Windows
scripts/start-dev.bat

# Linux/Mac
chmod +x scripts/start-dev.sh
./scripts/start-dev.sh
```

#### Start Services Individually

**Backend (FastAPI):**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (React):**
```bash
cd frontend
npm install
npm start
```

**Streamlit App (Alternative UI):**
```bash
streamlit run src/app.py
```

### Option 3: Using the API Programmatically

```python
import requests

# Query the AI pipeline
response = requests.post("http://localhost:8000/api/v1/query/query", 
                        json={"query": "What's the weather in London?"})
print(response.json())

# Weather-specific endpoint
response = requests.post("http://localhost:8000/api/v1/weather/weather",
                        json={"city": "London"})
print(response.json())

# RAG-specific endpoint
response = requests.post("http://localhost:8000/api/v1/rag/rag",
                        json={"question": "What is RAG?"})
print(response.json())
```

## Project Structure

```
ai-engineer-assignment/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py
│   │   │   │   ├── query.py
│   │   │   │   ├── weather.py
│   │   │   │   └── rag.py
│   │   │   └── __init__.py
│   │   ├── core/         # Core functionality
│   │   │   ├── config.py
│   │   │   ├── cors.py
│   │   │   ├── dependencies.py
│   │   │   └── models.py
│   │   ├── main.py       # FastAPI app
│   │   └── __init__.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API services
│   │   ├── types/        # TypeScript types
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── src/                   # Original source code (Streamlit)
│   ├── __init__.py
│   ├── app.py            # Streamlit application
│   ├── config.py
│   ├── data_loader.py
│   ├── embeddings.py
│   ├── langgraph_engine.py
│   ├── llm_wrappers.py
│   ├── rag_chain.py
│   ├── vectorstore.py
│   └── weather.py
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Development scripts
├── data/                  # Data files
├── faiss_index/           # FAISS index storage
├── docker-compose.yml     # Docker orchestration
├── nginx.conf            # Nginx configuration
├── .gitignore
├── env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Lint code
flake8 src tests
mypy src

# Run all quality checks
pre-commit run --all-files
```

### Adding New Features

1. **New API Endpoints**: Add new endpoints in `backend/app/api/endpoints/`
2. **New React Components**: Add components in `frontend/src/components/`
3. **New LangGraph Nodes**: Add new processing nodes to `src/langgraph_engine.py`
4. **New Data Sources**: Extend the data loading in `src/data_loader.py`
5. **New LLM Providers**: Add wrappers in `src/llm_wrappers.py`

## API Reference

### Backend API Endpoints

- `POST /api/v1/query/query` - Main query endpoint (weather or RAG)
- `POST /api/v1/weather/weather` - Weather-specific endpoint
- `GET /api/v1/weather/weather/{city}` - Get weather by city
- `POST /api/v1/rag/rag` - RAG-specific endpoint
- `GET /api/v1/health/health` - Health check

### Core Classes

- `LangGraphEngine`: Main workflow orchestrator
- `Settings`: Configuration management
- `GraphState`: LangGraph state definition

### Key Functions

- `build_rag_chain()`: Creates RAG processing chain
- `get_weather_for_city()`: Fetches weather data
- `build_faiss_from_docs()`: Creates vector store from documents

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root and have installed the package
2. **API Key Errors**: Verify your `.env` file has the correct API keys
3. **PDF Loading Issues**: Ensure the PDF file exists and is not corrupted
4. **Memory Issues**: For large PDFs, consider using a smaller embedding model

### Getting Help

- Check the test files for usage examples
- Review the configuration in `config.py`
- Ensure all dependencies are installed correctly
