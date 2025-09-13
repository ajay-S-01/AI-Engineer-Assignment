# src/rag_chain.py
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import FAISS


class NoDocsRAG:
    def run(self, query: str) -> str:
        return "No PDF content available. Please upload a non-empty PDF or update `PDF_PATH`."

def build_rag_chain(llm, vectorstore: FAISS | None, top_k: int = 4):
    if not vectorstore:
        return NoDocsRAG()
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa
