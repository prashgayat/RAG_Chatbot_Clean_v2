from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List
import streamlit as st
import os

# 1. ✅ Add/append chunks to FAISS vectorstore
def add_to_vectorstore(chunks: List[Document]):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if "vectorstore" in st.session_state and st.session_state.vectorstore is not None:
        st.session_state.vectorstore.add_documents(chunks)
    else:
        st.session_state.vectorstore = FAISS.from_documents(chunks, embedding_model)

# 2. ✅ Retrieve using hybrid search
def hybrid_retriever(query, k=5, rerank=False):
    if "vectorstore" not in st.session_state or st.session_state.vectorstore is None:
        raise ValueError("Vectorstore not initialized. Please upload documents first.")

    faiss_store = st.session_state.vectorstore

    # Semantic results
    semantic_results = faiss_store.similarity_search(query, k=k)

    # Keyword retriever from same documents
    all_docs = list(faiss_store.docstore._dict.values())
    bm25 = BM25Retriever.from_documents(all_docs)
    bm25.k = k
    keyword_results = bm25.get_relevant_documents(query)

    # Merge + de-dupe
    combined = {doc.page_content: doc for doc in (semantic_results + keyword_results)}
    final_docs = list(combined.values())

    if rerank:
        return rerank_documents(query, final_docs)

    return final_docs

# 3. 🧠 Optional: OpenAI re-ranker
def rerank_documents(query: str, documents: List[Document]) -> List[Document]:
    import openai
    from operator import itemgetter
    from dotenv import load_dotenv
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment.")

    # Format docs into text chunks for re-ranking
    texts = [doc.page_content for doc in documents]
    joined_contexts = "\n\n".join(f"{i+1}. {text}" for i, text in enumerate(texts))

    prompt = f"""You are a helpful assistant. Rank the following excerpts based on how well they answer the query.

Query: {query}

Excerpts:
{joined_contexts}

Return the ranking as a list of numbers (e.g., 2,1,3).
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a ranking assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    ranks = response.choices[0].message.content.strip()
    try:
        order = [int(i)-1 for i in ranks.split(",") if i.strip().isdigit()]
        reranked = [documents[i] for i in order if 0 <= i < len(documents)]
        return reranked
    except Exception as e:
        print(f"Re-ranking failed: {e}")
        return documents
