import os
import re
import tempfile
import streamlit as st
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredFileLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    Docx2txtLoader
)
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from semantic_text_splitter import TextSplitter as SemanticSplitter
from docx import Document as DocxReader  # Final fallback

# Domain-specific keywords
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

def extract_with_python_docx(path, filename):
    try:
        docx = DocxReader(path)
        paragraphs = [p.text.strip() for p in docx.paragraphs if p.text.strip()]
        if not paragraphs:
            return []
        text = "\n".join(paragraphs)
        print(f"✅ Fallback: Extracted {len(paragraphs)} paragraphs using python-docx from {filename}")
        return [Document(page_content=text, metadata={"source": filename})]
    except Exception as e:
        print(f"❌ python-docx fallback failed: {e}")
        return []

def load_documents(uploaded_files):
    documents = []
    for file in uploaded_files:
        try:
            suffix = os.path.splitext(file.name)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            loaded_docs = []

            if suffix == ".pdf":
                loader = PyPDFLoader(tmp_path)
                loaded_docs = loader.load()

            elif suffix == ".txt":
                loader = UnstructuredFileLoader(tmp_path)
                loaded_docs = loader.load()

            elif suffix == ".docx":
                loader = UnstructuredWordDocumentLoader(tmp_path)
                loaded_docs = loader.load()

                if not loaded_docs:
                    print(f"⚠️ Unstructured failed. Trying docx2txt fallback for: {file.name}")
                    fallback_loader = Docx2txtLoader(tmp_path)
                    loaded_docs = fallback_loader.load()

                if not loaded_docs:
                    print(f"⚠️ docx2txt also failed. Using python-docx fallback for: {file.name}")
                    loaded_docs = extract_with_python_docx(tmp_path, file.name)

            elif suffix == ".xlsx":
                loader = UnstructuredExcelLoader(tmp_path)
                loaded_docs = loader.load()

            else:
                print(f"⚠️ Unsupported file type: {file.name}")
                continue

            if not loaded_docs:
                print(f"⚠️ Warning: No content extracted from {file.name}.")
            else:
                print(f"✅ Loaded {len(loaded_docs)} raw documents from {file.name}")
                for i, doc in enumerate(loaded_docs[:3]):
                    print(f"Preview [{i+1}]:", doc.page_content[:200])
                documents.extend(loaded_docs)

            os.remove(tmp_path)

        except Exception as e:
            print(f"❌ Error loading {file.name}: {str(e)}")
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
        print(f"⚠️ All extraction methods failed for: {file.name}")
        raise ValueError(f"No content found in {file.name}")

    print(f"✅ Proceeding to chunk {len(documents)} documents from {file.name}")
    splitter = HybridTextSplitter()
    chunks = splitter.split_documents(documents)

    if not chunks:
        print("⚠️ Chunking failed: no output after splitting.")
        raise ValueError("No chunks created during splitting.")

    print(f"✅ Created {len(chunks)} chunks.")
    add_to_vectorstore(chunks)
