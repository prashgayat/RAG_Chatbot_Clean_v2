#LLM answer

import os
import openai
from dotenv import load_dotenv

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain.docstore.document import Document

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔹 Step 1: Return docs as-is for use in hybrid retrievers
def embed_and_store(docs):
    return docs

# 🔹 Step 2: Build the hybrid retriever (BM25 + FAISS)
def get_hybrid_retriever(docs):
    bm25 = BM25Retriever.from_documents(docs)
    bm25.k = 5

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    faiss_retriever = vectorstore.as_retriever(search_type="mmr")
    faiss_retriever.k = 5

    return EnsembleRetriever(retrievers=[bm25, faiss_retriever], weights=[0.5, 0.5])

# 🔹 Step 3: Use OpenAI GPT to rerank top-k retrieved chunks
def rerank_documents_with_gpt(query, documents, top_k=3):
    prompt = f"""You are a helpful assistant tasked with re-ranking chunks of a document based on how well they answer the following question:

Question: "{query}"

Rank the following document chunks by how relevant they are (most relevant first). Output only the top {top_k} most relevant chunks.

Chunks:
""" + "\n\n".join([f"[{i+1}]: {doc.page_content}" for i, doc in enumerate(documents)])

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

# 🔹 Step 4: Build a fallback-aware QA chain using reranked chunks
def get_reranked_qa_chain_with_fallback(docs, query):
    retriever = get_hybrid_retriever(docs)
    initial_docs = retriever.get_relevant_documents(query)
    reranked_docs = rerank_documents_with_gpt(query, initial_docs)

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

    response = llm.predict(prompt)

    answer, confidence = "", ""
    for line in response.splitlines():
        if line.lower().startswith("answer:"):
            answer = line.split(":", 1)[1].strip()
        elif line.lower().startswith("confidence:"):
            confidence = line.split(":", 1)[1].strip().lower()

    if "low" in confidence:
        return "⚠️ I'm not confident in an answer based on the document. Please try rephrasing or uploading a different file."
    return answer
