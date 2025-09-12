# src/app.py
import streamlit as st
from src.config import settings
from src.data_loader import load_and_split_pdf
from src.embeddings import get_embeddings
from src.vectorstore import build_faiss_from_docs, load_faiss
from src.llm_wrappers import get_llm
from src.rag_chain import build_rag_chain
from src.langgraph_engine import LangGraphEngine
import os

st.set_page_config(page_title="AI Pipeline Demo", layout="wide")
st.title("AI Pipeline: Weather + PDF RAG Demo")

@st.cache_resource
def init_pipeline():
    # Load docs & build FAISS (or load if exists)
    embeddings = get_embeddings()
    persist_path = settings.FAISS_INDEX_PATH
    # Try load if exists otherwise build from PDF
    if os.path.exists(persist_path):
        vectorstore = load_faiss(persist_path, embeddings)
    else:
        docs = load_and_split_pdf(settings.PDF_PATH)
        vectorstore = build_faiss_from_docs(docs, embeddings, persist_path=persist_path)
    # LLM: default is ChatOpenAI or user-specified
    llm = get_llm()
    rag = build_rag_chain(llm, vectorstore)
    engine = LangGraphEngine(rag_chain=rag, llm=llm, openweather_api_key=settings.OPENWEATHER_API_KEY)
    return engine

engine = init_pipeline()

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question about the PDF or weather (e.g., 'What's the weather in London?')", key="query")
if st.button("Send"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            try:
                resp = engine.handle(query)
            except Exception as e:
                resp = f"Error: {e}"
        st.session_state.history.append((query, resp))

for q, a in st.session_state.history[::-1]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Assistant:** {a}")
    st.markdown("---")
