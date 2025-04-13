import streamlit as st
from ragify import chat_with_rag_chain
from utils.constants import CHAT_USER_ICON, CHAT_AI_ICON

def load_chat_history():
    """
    Displays the chat history in the Streamlit app.
    """
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_user_prompt(prompt):
    """
    Handles the user prompt and generates a response using the RAG chain.
    """
    # Add user message to chat history
    st.session_state.messages.append({"role": CHAT_USER_ICON, "content": prompt})
    with st.chat_message(CHAT_USER_ICON):
        st.markdown(prompt)

    # Generate response using RAG chain
    with st.spinner("Generating response..."):
        response = chat_with_rag_chain(st.session_state.rag_chain, prompt)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": CHAT_AI_ICON, "content": response})
    with st.chat_message(CHAT_AI_ICON):
        st.markdown(response)
        if len(st.session_state.messages) == 2:
            st.rerun()