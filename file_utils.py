import os
import tempfile
from pathlib import Path
import streamlit as st

from langchain_community.document_loaders import (
    UnstructuredFileLoader,
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

from langchain_core.documents import Document
from Hybrid_splitter import HybridTextSplitter as TextSplitter  # ✅ Semantic + rule-based splitting


def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    if hasattr(uploaded_file, "name"):
        save_path = os.path.join(temp_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
    else:
        save_path = str(uploaded_file)
    return save_path


def load_file(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(path)
    elif ext == ".txt":
        return TextLoader(path, encoding="utf-8")
    elif ext == ".docx":
        return Docx2txtLoader(path)
    else:
        return UnstructuredFileLoader(path)


def file_loader(uploaded_files, chunk_size=300, chunk_overlap=50):
    all_chunks = []

    for uploaded_file in uploaded_files:
        try:
            file_path = save_uploaded_file(uploaded_file)
            st.success(f"{Path(file_path).name} uploaded successfully")

            loader = load_file(file_path)
            docs = loader.load()

            splitter = TextSplitter(chunk_size=chunk_size, overlap=chunk_overlap)
            chunks = splitter.split_documents(docs)

            all_chunks.extend(chunks)
        except Exception as e:
            st.error(f"🔥 Error processing file: {e}")

    return all_chunks
