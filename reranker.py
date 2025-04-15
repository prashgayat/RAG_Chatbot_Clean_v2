
from sentence_transformers import CrossEncoder

def rerank_results(query, documents):
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = [[query, doc.page_content] for doc in documents]
    scores = model.predict(pairs)
    scored_docs = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored_docs[:5]]
