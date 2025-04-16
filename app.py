import streamlit as st
import uuid
from file_utils import process_file
from text_split.Hybrid_splitter import HybridTextSplitter
from retriever_utils import hybrid_retriever
from llm_answer import llm_answer
from memory_utils import get_memory

# ---- Streamlit UI Setup ----
st.set_page_config(page_title="📚 Robust RAG Chatbot with Hybrid Search + Re-ranking")
st.title("📚 Robust RAG Chatbot with Hybrid Search + Re-ranking")

uploaded_file = st.file_uploader("Upload documents", type=["pdf", "txt", "docx", "xlsx"])

if uploaded_file:
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"📄 Saved uploaded file to: {file_path}")

    # Step 1: Load + Parse
    documents = process_file(file_path)

    # Step 2: Hybrid Chunking
    splitter = HybridTextSplitter()
    chunks = splitter.split_documents(documents)

    if not chunks:
        st.error("❗ No text chunks created. Please check the document format or content.")
    else:
        st.success(f"✅ Document '{file_path}' uploaded and processed successfully!")

        # Step 3: Session Memory Setup
        session_id = st.session_state.get("session_id", str(uuid.uuid4()))
        st.session_state["session_id"] = session_id
        memory = get_memory(session_id)

        # Step 4: Ask Questions
        user_question = st.text_input("Ask a question about the document:")

        if user_question:
            # ⚠️ Replace these with actual stores if not wired
            vectorstore = None
            keyword_index = None

            # Step 5: Hybrid Retrieve + Answer
            docs = hybrid_retriever(user_question, vectorstore, keyword_index)
            answer = llm_answer(user_question, docs, memory)

            st.markdown("### 🤖 Answer")
            st.write(answer)

# Optional: Memory Reset
if st.button("🔄 Reset Memory"):
    st.session_state["session_id"] = str(uuid.uuid4())
    st.success("🧠 Conversation memory reset.")
