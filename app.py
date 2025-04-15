import os
import uuid
import streamlit as st
from file_utils import file_loader
from llm_answer import embed_and_store, get_reranked_qa_chain_with_fallback
from memory_utils import reset_chat_history

st.set_page_config(page_title="RAG Chatbot", page_icon="😎")
st.title("🧠 RAG Chatbot with Hybrid Search + GPT Re-ranking")

# Unique session tracking
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "stored_docs" not in st.session_state:
    st.session_state.stored_docs = []

st.markdown("**Upload a document**")
uploaded_files = st.file_uploader("", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    docs = file_loader(uploaded_files)
    if not docs:
        st.error("❗ No text chunks created. Please check the document format or content.")
    else:
        st.session_state.stored_docs.extend(docs)
        st.success(f"✅ Loaded {len(docs)} chunks from uploaded file(s).")

# Memory reset button
if st.button("Reset Memory"):
    reset_chat_history(st.session_state.session_id)
    st.success("💚 Memory reset for this session.")

# Chat interface
if st.session_state.stored_docs:
    with st.form("question_form"):
        query = st.text_input("Ask a question or follow-up:", key="user_input")
        submitted = st.form_submit_button("Submit")

    if submitted and query:
        with st.spinner("📡 Retrieving documents..."):
            response = get_reranked_qa_chain_with_fallback(
                st.session_state.stored_docs,
                query,
                session_id=st.session_state.session_id
            )
            st.markdown("**💬 Response:**")
            st.write(response)

