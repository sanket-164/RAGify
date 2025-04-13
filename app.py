import streamlit as st
from ragify import chat_with_rag_chain
from input_config import select_input
from sidebar import sidebar
from session import session_initialization

# Main function to run the Streamlit app
def main():
    st.title("🤖 RAGify")

    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False

    if st.session_state.show_sidebar:
        sidebar()
    else:
        select_input()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # User input for chat
    if st.session_state.rag_chain is not None:
        if prompt := st.chat_input("Ask a question about the content..."):

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response using RAG chain
            with st.spinner("Generating response..."):
                response = chat_with_rag_chain(st.session_state.rag_chain, prompt)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

if __name__ == "__main__":
    session_initialization()
    main()