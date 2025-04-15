# llm_answer.py

from dotenv import load_dotenv
load_dotenv()
import os
import openai

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain.docstore.document import Document
from memory_utils import store_memory, retrieve_memory

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_and_store(docs):
    return docs

def get_hybrid_retriever(docs):
    bm25 = BM25Retriever.from_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    faiss_retriever = vectorstore.as_retriever(search_type="mmr")

    return EnsembleRetriever(retrievers=[bm25, faiss_retriever], weights=[0.5, 0.5])

def rerank_documents_with_gpt(query, documents, top_k=3):
    if not documents:
        return []

    prompt = f"""You are a helpful assistant tasked with re-ranking chunks of a document based on how well they answer the following question:

Question: "{query}"

Rank the following document chunks by how relevant they are (most relevant first). Output only the top {top_k} most relevant chunks.

Chunks:
""" + "\n\n".join([f"[{i+1}]: {doc.page_content}" for i, doc in enumerate(documents)])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0
        )

        output = response.choices[0].message["content"]

        selected_chunks = []
        for i in range(1, len(documents)+1):
            if f"[{i}]" in output:
                selected_chunks.append(documents[i-1])
            if len(selected_chunks) == top_k:
                break

        return selected_chunks
    except Exception as e:
        print("⚠️ GPT reranking failed:", e)
        return []

def get_reranked_qa_chain_with_fallback(docs, query, session_id=None):
    retriever = get_hybrid_retriever(docs)
    initial_docs = retriever.get_relevant_documents(query)
    reranked_docs = rerank_documents_with_gpt(query, initial_docs)

    if not reranked_docs:
        return "⚠️ GPT could not rerank any relevant chunks confidently."

    llm = ChatOpenAI(temperature=0.2)

    context = "\n\n".join([doc.page_content for doc in reranked_docs])
    prompt = f"""
You are a factual assistant. Answer the question using **only** the context below.
If the context does not contain enough information to confidently answer, say "I don't know."

Context:
{context}

Question: {query}

Respond with:
- "Answer: <your answer>"
- "Confidence: High" or "Confidence: Low"
"""

    try:
        response = llm.predict(prompt)
    except Exception as e:
        return f"⚠️ LLM failed to respond: {e}"

    print("🔍 Final LLM Response:\n", response)

    answer, confidence = "", ""
    for line in response.splitlines():
        if line.lower().startswith("answer:"):
            answer = line.split(":", 1)[1].strip()
        elif line.lower().startswith("confidence:"):
            confidence = line.split(":", 1)[1].strip().lower()

    if session_id:
        store_memory(session_id, query, answer)

    if "low" in confidence or not answer:
        return "⚠️ I'm not confident in an answer based on the document. Please try rephrasing or uploading a different file."
    return answer