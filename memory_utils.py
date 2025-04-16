import streamlit as st
import uuid

def initialize_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "memory" not in st.session_state:
        st.session_state.memory = {}

    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_memory(session_id: str):
    memory = st.session_state.get("memory", {})
    return memory.get(session_id, [])

def update_memory(session_id: str, message: str):
    if "memory" not in st.session_state:
        st.session_state.memory = {}

    if session_id not in st.session_state.memory:
        st.session_state.memory[session_id] = []

    st.session_state.memory[session_id].append(message)
