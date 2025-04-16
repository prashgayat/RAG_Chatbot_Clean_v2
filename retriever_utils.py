def hybrid_retriever(query, vectorstore, keyword_index, top_k=5):
    print(f"🔍 Running hybrid retrieval for: '{query}'")

    # Semantic
    semantic_docs = vectorstore.similarity_search(query, k=top_k)
    print(f"📘 Semantic results: {len(semantic_docs)}")

    # Keyword
    keyword_docs = keyword_index.similarity_search(query, k=top_k)
    print(f"📗 Keyword results: {len(keyword_docs)}")

    # Combine
    combined = semantic_docs + keyword_docs
    print(f"📥 Total combined before re-ranking: {len(combined)}")
    for i, doc in enumerate(combined[:3]):
        print(f"Doc {i+1} Preview:\n{doc.page_content[:300]}...\n")

    # Re-rank
    from reranker_utils import rerank_results  # assumed import
    reranked = rerank_results(query, combined)

    print(f"🏁 Top {len(reranked)} reranked results")
    for i, doc in enumerate(reranked[:2]):
        print(f"Reranked Doc {i+1} Preview:\n{doc.page_content[:300]}...\n")

    return reranked
