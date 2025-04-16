import re
from typing import List
from langchain.schema import Document
from semantic_text_splitter import TextSplitter

class HybridTextSplitter:
    def __init__(self, keywords=None, chunk_size=300, chunk_overlap=50):
        self.keywords = keywords or [
            "agreement", "obligation", "terms", "party", "confidential", "contract",
            "purpose", "responsibility", "definition", "scope", "termination", "right", "project"
        ]
        # ✅ Correct semantic splitter initialization
        self.semantic_splitter = TextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def _keyword_split(self, text: str) -> List[str]:
        try:
            pattern = r"|".join([rf"\b{k}\b" for k in self.keywords])
            splits = re.split(pattern, text, flags=re.IGNORECASE)
            print(f"🔑 Keyword-based splits: {len(splits)}")
            return [s.strip() for s in splits if s.strip()]
        except Exception as e:
            print(f"❗ Keyword split failed: {e}")
            return [text]

    def split_documents(self, documents: List[Document]) -> List[Document]:
        all_chunks = []

        for doc in documents:
            text = doc.page_content.strip()
            if not text:
                continue

            try:
                keyword_chunks = self._keyword_split(text)
                semantic_chunks = self.semantic_splitter.create_documents(keyword_chunks)

                print(f"🧠 Semantic chunks created: {len(semantic_chunks)}")
                for i, chunk in enumerate(semantic_chunks[:3]):
                    print(f"Chunk {i+1} Preview:\n{chunk.page_content[:300]}...\n")

                all_chunks.extend(semantic_chunks)
            except Exception as e:
                print(f"❗ Error while splitting document: {e}")

        print(f"📦 Total Chunks Returned: {len(all_chunks)}")
        return all_chunks
