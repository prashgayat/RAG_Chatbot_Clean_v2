from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

def prepare_retrievers(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("❗ No chunks created from the uploaded documents. Please check the file content.")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_store = FAISS.from_documents(chunks, embeddings)
    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = 5

    return faiss_store, bm25, chunks


