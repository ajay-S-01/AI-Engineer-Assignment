# src/rag_chain.py
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import FAISS

def build_rag_chain(llm, vectorstore: FAISS, top_k: int = 4):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa
