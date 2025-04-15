from semantic_text_splitter import TextSplitter as SemanticTextSplitter
from typing import List, Dict
import re

class HybridTextSplitter:
    def __init__(self, chunk_size: int = 300, overlap: int = 50, keywords: List[str] = None):
        self.semantic_splitter = SemanticTextSplitter(
            capacity=chunk_size,
            overlap=overlap,
            separators=["\n\n", "\n", ". "],
            preserve_separators=False
        )
        self.keywords = keywords or ["Habit", "Principle", "Mission", "Character", "Effectiveness"]

    def _keyword_split(self, text: str) -> List[str]:
        pattern = r"|".join([fr"(?i)(?<=\b{kw}\b)" for kw in self.keywords])
        parts = re.split(pattern, text)
        return [part.strip() for part in parts if part.strip()]

    def split_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        all_chunks = []
        for doc in documents:
            text = doc.get("page_content", "")

            # First use keyword-based splitting
            keyword_chunks = self._keyword_split(text)

            # Then apply semantic splitting on each keyword chunk
            for chunk in keyword_chunks:
                semantically_split = self.semantic_splitter.split_text(chunk)
                for sub_chunk in semantically_split:
                    all_chunks.append({"page_content": sub_chunk})

        return all_chunks