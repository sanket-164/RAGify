import streamlit as st
from ragify import chat_with_rag_chain

def load_chat_history():
    """
    Displays the chat history in the Streamlit app.
    """
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("🧑"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("🤖"):
                st.markdown(msg["content"])

def handle_user_prompt(prompt):
    """
    Handles the user prompt and generates a response using the RAG chain.
    """
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("🧑"):
        st.markdown(prompt)

    # Generate response using RAG chain
    with st.spinner("Generating response..."):
        response = chat_with_rag_chain(st.session_state.rag_chain, prompt)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("🤖"):
        st.markdown(response)
        if len(st.session_state.messages) == 2:
            st.rerun()