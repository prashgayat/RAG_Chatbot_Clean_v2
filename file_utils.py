import os
import tempfile
from pathlib import Path
import streamlit as st
from langchain_community.document_loaders import (
    UnstructuredFileLoader,
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_core.documents import Document
from semantic_text_splitter import TextSplitter


def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())
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


def file_loader(uploaded_files, chunk_size=300):
    all_chunks = []
    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    for uploaded_file in uploaded_files:
        try:
            file_path = save_uploaded_file(uploaded_file)
            st.success(f"{Path(file_path).name} uploaded successfully")
            loader = load_file(file_path)
            docs = loader.load()

            splitter = TextSplitter(chunk_size)
            chunks = splitter.split_documents(docs)
            all_chunks.extend(chunks)
        except Exception as e:
            st.error(f"🔥 Error processing file: {e}")
    return all_chunks
