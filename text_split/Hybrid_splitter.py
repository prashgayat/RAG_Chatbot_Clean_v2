# Hybrid_splitter.py

from semantic_text_splitter import TextSplitter as SemanticTextSplitter
from typing import List
import re
from langchain_core.documents import Document


class HybridTextSplitter:
    def __init__(self, chunk_size: int = 300, overlap: int = 50, keywords: List[str] = None):
        self.semantic_splitter = SemanticTextSplitter(
            capacity=chunk_size,
            overlap=overlap
        )
        self.keywords = keywords or ["Habit", "Principle", "Mission", "Character", "Effectiveness"]

    def _keyword_split(self, text: str) -> List[str]:
        # Create a regex pattern to split before the keywords (case-insensitive)
        pattern = r"|".join([fr"(?i)(?=\b{re.escape(kw)}\b)" for kw in self.keywords])
        parts = re.split(pattern, text)
        return [part.strip() for part in parts if part.strip()]

    def split_documents(self, documents: List[Document]) -> List[dict]:
        all_chunks = []
        for doc in documents:
            text = doc.page_content

            # Step 1: Keyword-based split (domain-specific)
            keyword_chunks = self._keyword_split(text)

            # Step 2: Semantic split on keyword chunks
            for chunk in keyword_chunks:
                semantic_chunks = self.semantic_splitter.split_text(chunk)
                for sub_chunk in semantic_chunks:
                    all_chunks.append({"page_content": sub_chunk})

        return all_chunks
