import os
import streamlit as st
from semantic_text_splitter import TextSplitter
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredFileLoader

def file_loader(uploaded_file):
    try:
        # ✅ Ensure upload directory exists
        upload_dir = "uploaded_docs"
        os.makedirs(upload_dir, exist_ok=True)

        # ✅ Save the uploaded file to disk
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ✅ Load file content using UnstructuredFileLoader
        loader = UnstructuredFileLoader(file_path)
        raw_docs = loader.load()

        if not raw_docs:
            st.error("⚠️ Document could not be parsed. Try uploading a different file.")
            return []

        return split_documents(raw_docs)

    except Exception as e:
        st.error(f"🔥 Error: {str(e)}")
        return []

def split_documents(documents):
    # ✅ Initialize the semantic splitter with sentence-transformers model
    splitter = TextSplitter(model="sentence-transformers/all-MiniLM-L6-v2")

    all_chunks = []
    for doc in documents:
        chunks = splitter.chunks(
            doc.page_content,
            chunk_size=300,
            chunk_overlap=50
        )
        for chunk in chunks:
            all_chunks.append(Document(page_content=chunk))

    if not all_chunks:
        st.error("❌ No chunks were generated. Please try a simpler document or different format.")

    return all_chunks

