import streamlit as st
from datetime import datetime
from ragify import chat_with_rag_chain
from input_config import select_input
from sidebar import sidebar

# Initialize session state for chat history and RAG chain
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "processed_yt_urls" not in st.session_state:
    st.session_state.processed_yt_urls = []

if "processed_website_urls" not in st.session_state:
    st.session_state.processed_website_urls = []

if "persist_directory" not in st.session_state:
    st.session_state.persist_directory = f"./{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_vectorstore"

if "no_of_yt_urls" not in st.session_state:
    st.session_state.no_of_yt_urls = 0

if "no_of_website_urls" not in st.session_state:
    st.session_state.no_of_website_urls = 0

if "file_extensions" not in st.session_state:
    st.session_state.file_extensions = []

if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# Main function to run the Streamlit app
def main():
    st.title("🤖 RAGify")
    st.caption("Upload docs, links, or videos & get instant answers.")

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
    main()