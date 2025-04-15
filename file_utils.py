import os
import re
import tempfile
import streamlit as st
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
)
from semantic_text_splitter import TextSplitter as SemanticSplitter
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Domain-specific keywords for keyword-based splitting
SPLIT_KEYWORDS = [
    "summary", "conclusion", "recommendation", "introduction",
    "background", "objective", "finding", "decision", "judgment",
    "agreement", "confidentiality", "disclosure", "termination"
]

class HybridTextSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.semantic_splitter = SemanticSplitter(capacity=chunk_size)

    def keyword_split(self, text):
        pattern = r"\b(" + "|".join(map(re.escape, SPLIT_KEYWORDS)) + r")\b"
        return re.split(pattern, text, flags=re.IGNORECASE)

    def split_documents(self, documents: List[Document]) -> List[Document]:
        all_chunks = []
        for doc in documents:
            keyword_chunks = self.keyword_split(doc.page_content)
            for chunk in keyword_chunks:
                semantic_chunks = self.semantic_splitter.chunks(chunk)
                for sc in semantic_chunks:
                    all_chunks.append(Document(page_content=sc, metadata=doc.metadata))
        return all_chunks

def load_documents(uploaded_files):
    documents = []
    for file in uploaded_files:
        try:
            suffix = os.path.splitext(file.name)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            if suffix == ".pdf":
                loader = PyPDFLoader(tmp_path)
            elif suffix == ".txt":
                loader = TextLoader(tmp_path)
            elif suffix == ".docx":
                loader = Docx2txtLoader(tmp_path)
            elif suffix == ".xlsx":
                loader = UnstructuredExcelLoader(tmp_path)
            else:
                continue

            documents.extend(loader.load())
            os.remove(tmp_path)
        except Exception as e:
            print(f"Error loading {file.name}: {str(e)}")
    return documents

def add_to_vectorstore(chunks: List[Document]):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if "vectorstore" in st.session_state and st.session_state.vectorstore is not None:
        st.session_state.vectorstore.add_documents(chunks)
    else:
        st.session_state.vectorstore = FAISS.from_documents(chunks, embedding_model)

def process_file(file):
    documents = load_documents([file])
    if not documents:
        raise ValueError(f"No content found in {file.name}")

    splitter = HybridTextSplitter()
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No chunks created during splitting.")

    add_to_vectorstore(chunks)
