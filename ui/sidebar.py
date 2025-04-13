import os
import streamlit as st
from ragify import (
    chunk_pdf,
    chunk_word_doc,
    chunk_pptx,
    chunk_txt_file,
    chunk_excel,
    chunk_youtube_video,
    chunk_website,
    create_vectorstore,
    create_rag_chain,
)
from utils.session import reset_session
from utils.constants import FILE_UPLOAD_DIRECTORY

# Uploads directory
os.makedirs(FILE_UPLOAD_DIRECTORY, exist_ok=True)

def check_content_changed(uploaded_filenames, yt_urls, website_urls):
    """
    Check if the content has changed based on the uploaded files, YouTube URLs, and website URLs.
    """
    
    # Check if any of the inputs have changed
    if (
        uploaded_filenames == [] and yt_urls == [] and website_urls == []
    ):
        return False
    
    for uploaded_file in uploaded_filenames:
        if uploaded_file not in st.session_state.processed_files:
            return True
    
    for yt_url in yt_urls:
        if yt_url and yt_url not in st.session_state.processed_yt_urls:
            return True
    
    for website_url in website_urls:
        if website_url and website_url not in st.session_state.processed_website_urls:
            return True
        
    return False

@st.dialog("Are you sure you want to clear chats?")
def clear_chat():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yeah, don't care", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("No, want to read them", use_container_width=True):
            st.rerun()

def sidebar():
    """
    Sidebar for the Streamlit app to handle file uploads and URL inputs.
    """
    with st.sidebar.expander("Clear Data", expanded=False):
        st.error("This will clear all processed content and chat history.\n Are you sure?")
        if st.button("Yes", use_container_width=True):
            reset_session()
            st.session_state.show_balloons = True
            st.rerun()
            
    # Sidebar for user inputs
    uploaded_files = []
    if len(st.session_state.file_extensions) > 0:
        uploaded_files = st.sidebar.file_uploader(
            "Upload files", type=st.session_state.file_extensions, accept_multiple_files=True
        )

    # Multiple YouTube URLs
    yt_urls = []
    if st.session_state.no_of_yt_urls > 0:
        st.sidebar.markdown("### YouTube Links")
        for i in range(st.session_state.no_of_yt_urls):
            yt_url = st.sidebar.text_input("YouTube URL", placeholder=f"YouTube Video URL {i+1}", label_visibility="collapsed")
            if yt_url:
                yt_urls.append(yt_url)

    # Multiple Website URLs
    website_urls = []
    if st.session_state.no_of_website_urls > 0:
        st.sidebar.markdown("### Website Links")
        for i in range(st.session_state.no_of_website_urls):
            site_url = st.sidebar.text_input("Webiste URL", placeholder=f"Website URL {i+1}", label_visibility="collapsed")
            if site_url:
                website_urls.append(site_url)

    uploaded_filenames = [f.name for f in uploaded_files]
    
    if st.sidebar.button("Start Processing", use_container_width=True, disabled=not check_content_changed(uploaded_filenames, yt_urls, website_urls)):
        all_chunks = []

        try:
            # Process uploaded files
            if uploaded_files:
                uploaded_filenames = [f.name for f in uploaded_files]

                if uploaded_filenames != st.session_state.processed_files:

                    with st.spinner("Processing Content..."):
                        for uploaded_file in uploaded_files:
                            if uploaded_file.name not in st.session_state.processed_files:
                                # Get the file extension
                                filename = uploaded_file.name
                                ext = os.path.splitext(filename)[1].lower()

                                # Save the file temporarily
                                save_path = os.path.join(FILE_UPLOAD_DIRECTORY, filename)
                                with open(save_path, "wb") as f:
                                    f.write(uploaded_file.read())

                                print(f"Processing file: {filename} with extension: {ext}")

                                # Call the appropriate chunking function
                                if ext == ".pdf":
                                    chunks = chunk_pdf(save_path)
                                elif ext == ".docx":
                                    chunks = chunk_word_doc(save_path)
                                elif ext == ".pptx":
                                    chunks = chunk_pptx(save_path)
                                elif ext == ".txt":
                                    chunks = chunk_txt_file(save_path)
                                elif ext == ".xlsx":
                                    chunks = chunk_excel(save_path)
                                else:
                                    st.error(f"Unsupported file type: {ext}")
                                    continue

                                all_chunks.extend(chunks)

                    st.session_state.processed_files = uploaded_filenames

            # Process YouTube URLs
            for yt_url in yt_urls:
                if yt_url and yt_url not in st.session_state.processed_yt_urls:
                    
                    with st.spinner(f"Processing YouTube: {yt_url}"):
                        try:
                            chunks = chunk_youtube_video(yt_url)
                            all_chunks.extend(chunks)
                            st.session_state.setdefault("processed_yt_urls", []).append(yt_url)
                        except Exception:
                            st.error(f"Failed to process YouTube URL: {yt_url}")

            # Process website URLs
            for website_url in website_urls:
                if website_url and website_url not in st.session_state.processed_website_urls:
                    
                    with st.spinner(f"Processing Website: {website_url}"):
                        try:
                            if website_url.startswith("http"):
                                chunks = chunk_website(website_url)
                                all_chunks.extend(chunks)
                                st.session_state.setdefault("processed_website_urls", []).append(website_url)
                            else:
                                st.error(f"Invalid URL (must start with http/https): {website_url}")
                        except Exception:
                            st.error(f"Failed to process Website URL: {website_url}")
            
            # Create vector store and RAG chain if chunks are generated
            if len(all_chunks) > 0:
                vectorstore = create_vectorstore(all_chunks, st.session_state.persist_directory)
                st.session_state.rag_chain = create_rag_chain(vectorstore)
                st.session_state.toast_message = "Content processed successfully!"
                st.rerun()

        except Exception as e:
            st.error(f"Error processing content: {e}")
    
    if st.sidebar.button("Clear Chat" , type="primary", use_container_width=True, disabled=len(st.session_state.messages) == 0):
        clear_chat()
        
    if st.session_state.processed_files != []:
        with st.sidebar.status("Uploaded Files", state="complete"):
            for uploaded_file in st.session_state.processed_files:
                st.write(f"- {uploaded_file}")
    
    if st.session_state.processed_yt_urls != []:
        with st.sidebar.status("YouTube URLs", state="complete"):
            for yt_url in st.session_state.processed_yt_urls:
                st.write(f"- {yt_url}")

    if st.session_state.processed_website_urls != []:
        with st.sidebar.status("Website URLs", state="complete"):
            for website_url in st.session_state.processed_website_urls:
                st.write(f"- {website_url}")