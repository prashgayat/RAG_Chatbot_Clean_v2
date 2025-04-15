import streamlit as st
import uuid

def initialize_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "memory" not in st.session_state:
        st.session_state.memory = {}

    if "messages" not in st.session_state:
        st.session_state.messages = []
