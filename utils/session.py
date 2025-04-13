import streamlit as st
from datetime import datetime

def session_initialization():
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

    if "content_changed" not in st.session_state:
        st.session_state.content_changed = False
    
    if "toast_message" not in st.session_state:
        st.session_state.toast_message = ""

def reset_session():
    st.session_state.messages = []
    st.session_state.rag_chain = None
    st.session_state.processed_files = []
    st.session_state.processed_yt_urls = []
    st.session_state.processed_website_urls = []
    st.session_state.persist_directory = f"./{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_vectorstore"
    st.session_state.show_balloons = False
    st.session_state.content_changed = False
    st.session_state.toast_message = ""