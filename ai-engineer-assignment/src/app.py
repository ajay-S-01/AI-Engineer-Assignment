import streamlit as st
import sys
import os


# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import settings
from src.data_loader import load_and_split_pdf
from src.embeddings import get_embeddings
from src.vectorstore import build_faiss_from_docs, load_faiss
from src.llm_wrappers import get_llm
from src.rag_chain import build_rag_chain
from src.langgraph_engine import LangGraphEngine
from pypdf.errors import EmptyFileError
from langsmith import traceable
import os



if settings.LANGCHAIN_API_KEY:
    st.sidebar.success("LangSmith tracing active ✅")
    st.sidebar.write(f"Project: {settings.LANGCHAIN_PROJECT}")
else:
    st.sidebar.warning("LangSmith tracing not detected ⚠️")
print("LangSmith Project:", os.getenv("LANGCHAIN_PROJECT"))
print("LangSmith API Key:", os.getenv("LANGCHAIN_API_KEY")[:10] + "...")

# --- Page setup ---
st.set_page_config(page_title="AI Pipeline Demo", layout="wide")

st.markdown(
    """
    <style>
    .user-msg {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 8px;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .assistant-msg {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 8px;
        max-width: 80%;
        float: left;
        clear: both;
    }
    .chat-box {
        max-height: 500px;
        overflow-y: auto;
        padding-right: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI Pipeline: Weather + PDF RAG Demo")

# --- Initialize pipeline ---
@st.cache_resource
def init_pipeline():
    embeddings = get_embeddings()
    persist_path = settings.FAISS_INDEX_PATH

    if os.path.exists(persist_path):
        vectorstore = load_faiss(persist_path, embeddings)
    else:
        try:
            docs = load_and_split_pdf(settings.PDF_PATH)
        except FileNotFoundError as e:
            st.error(f"PDF not found: {e}")
            docs = []
        except EmptyFileError as e:
            st.error(f"PDF is empty or unreadable: {e}")
            docs = []

        if not docs:
            vectorstore = None
        else:
            vectorstore = build_faiss_from_docs(docs, embeddings, persist_path=persist_path)

    llm = get_llm()
    rag = build_rag_chain(llm, vectorstore)
    engine = LangGraphEngine(rag_chain=rag, llm=llm, openweather_api_key=settings.OPENWEATHER_API_KEY)
    return engine

engine = init_pipeline()

@traceable  # logs the function call + input/output
def handle_query(query: str):
    return engine.handle(query)

# --- Sidebar info ---
with st.sidebar:
    st.header("Settings")
    st.write(f"**Active LLM Provider:** `{settings.LLM_PROVIDER.upper()}`")
    if settings.LLM_PROVIDER.lower() == "gemini":
        st.info("Using Google Gemini via API key")
    elif settings.LLM_PROVIDER.lower() == "openai":
        st.info("Using OpenAI via API key")

    st.write("---")
    st.caption("Ask me about the **PDF** or get the **current weather** for a city!")

# --- Chat state ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Chat input ---
st.subheader("Chat with the Assistant")
query = st.text_input("Type your question:", key="query")

col1, col2 = st.columns([1, 5])
with col1:
    send = st.button("Send")
with col2:
    clear = st.button("Clear Chat")

if send:
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            try:
                resp = handle_query(query)
            except Exception as e:
                resp = f"Error: {e}"
        st.session_state.history.append((query, resp))

if clear:
    st.session_state.history = []

# --- Chat history ---
st.subheader("Conversation History")
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for q, a in st.session_state.history[::-1]:
    st.markdown(f'<div class="user-msg">{q}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="assistant-msg">{a}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
