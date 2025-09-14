from langchain.schema import Document
from src.embeddings import get_embeddings
from src.vectorstore import build_faiss_from_docs

def test_build_faiss(tmp_path):
    docs = [Document(page_content="hello world", metadata={"source":"t1"}),
            Document(page_content="another document", metadata={"source":"t2"})]
    embeddings = get_embeddings()
    vs = build_faiss_from_docs(docs, embeddings, persist_path=str(tmp_path/"index"))
    # simple check: similarity_search returns results
    hits = vs.similarity_search("hello", k=1)
    assert len(hits) >= 1
