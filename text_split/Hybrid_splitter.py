# text_split/Hybrid_splitter.py

import re
from semantic_text_splitter import TextSplitter  # ✅ THIS WORKS as proven in split_test.py

class HybridTextSplitter:
    def __init__(self, keywords=None, capacity=1000, overlap=100):
        self.keywords = keywords if keywords else [
            "Section", "Chapter", "Habit", "Agreement", "Clause", "Article", "Step"
        ]
        self.capacity = capacity
        self.overlap = overlap

        # ✅ Correct initialization for semantic-text-splitter==0.25.1
        self.semantic_splitter = TextSplitter(capacity=self.capacity, overlap=self.overlap)

    def keyword_based_split(self, text):
        try:
            pattern = r"(?i)(?=\n*(?:" + "|".join(re.escape(k) for k in self.keywords) + r"))"
            parts = re.split(pattern, text)
            return [p.strip() for p in parts if p.strip()]
        except Exception as e:
            print(f"⚠️ Keyword-based splitting failed: {e}")
            return [text]

    def split(self, text):
        keyword_chunks = self.keyword_based_split(text)
        semantic_chunks = []
        for chunk in keyword_chunks:
            try:
                refined = self.semantic_splitter.split_text(chunk)
                semantic_chunks.extend(refined)
            except Exception as e:
                print(f"⚠️ Semantic split failed: {e}")
                semantic_chunks.append(chunk)
        print(f"✅ Hybrid split complete: {len(semantic_chunks)} chunks")
        return semantic_chunks

    def split_documents(self, documents):
        all_chunks = []
        for doc in documents:
            text = getattr(doc, "page_content", None)
            if text:
                all_chunks.extend(self.split(text))
            else:
                print("⚠️ Document missing 'page_content'")
        return all_chunks
