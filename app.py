import streamlit as st
import os
from dotenv import load_dotenv
from file_utils import process_file
from retriever_utils import hybrid_retriever
from llm_answer import llm_answer
from memory_utils import initialize_session

load_dotenv()

st.set_page_config(page_title="Robust RAG Chatbot with Hybrid Search + Re-ranking")
st.title("📚 Robust RAG Chatbot with Hybrid Search + Re-ranking")

# Initialize session
initialize_session()

# File uploader
uploaded_files = st.file_uploader(
    "Upload documents",
    type=["pdf", "txt", "docx", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):
            process_file(file)
    st.success("Documents uploaded and processed successfully!")

# Display previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field
user_input = st.chat_input("Ask a question about the uploaded documents...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm_answer(user_input, session_id=st.session_state.get("session_id"))
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Optional memory reset
if st.button("🔄 Reset Conversation Memory"):
    st.session_state.memory.clear()
    st.session_state.messages = []
    st.success("Memory has been reset.")
