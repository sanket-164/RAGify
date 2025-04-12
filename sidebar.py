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

# Define a permanent uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def sidebar():
    # Sidebar for user inputs
    uploaded_files = []
    if len(st.session_state.file_extensions) > 0:
        st.sidebar.header("Upload or Input URL")
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


    if st.sidebar.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.rag_chain = None
        st.session_state.uploaded_files = []
        st.session_state.processed_yt_urls = []
        st.session_state.processed_website_urls = []
        st.success("Chat cleared!")
        st.rerun()
    
    if st.sidebar.button("Clear Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.rag_chain = None
        st.session_state.uploaded_files = []
        st.session_state.processed_yt_urls = []
        st.session_state.processed_website_urls = []
        st.session_state.show_sidebar = False
        st.session_state.show_balloons = True
        st.rerun()

    if uploaded_files or yt_urls or website_urls:
        all_chunks = []  # List to store chunks from all sources
        content_changed = False

        try:
            # Process uploaded files
            if uploaded_files:
                uploaded_filenames = [f.name for f in uploaded_files]

                if uploaded_filenames != st.session_state.processed_files:
                    st.session_state.processed_files = uploaded_filenames
                    with st.spinner("Processing Content..."):
                        content_changed = True
                        for uploaded_file in uploaded_files:
                            # Get the file extension
                            filename = uploaded_file.name
                            ext = os.path.splitext(filename)[1].lower()

                            # Save the file temporarily
                            save_path = os.path.join(UPLOAD_DIR, filename)
                            with open(save_path, "wb") as f:
                                f.write(uploaded_file.read())

                            print(save_path)

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

                            # Add chunks to the combined list
                            all_chunks.extend(chunks)

            # Process YouTube URLs
            for yt_url in yt_urls:
                if yt_url and yt_url not in st.session_state.get("processed_yt_urls", []):
                    with st.spinner(f"Processing YouTube: {yt_url}"):
                        content_changed = True
                        try:
                            chunks = chunk_youtube_video(yt_url)
                            all_chunks.extend(chunks)
                            st.session_state.setdefault("processed_yt_urls", []).append(yt_url)
                        except Exception:
                            st.error(f"Failed to process YouTube URL: {yt_url}")

            # Process website URLs
            for website_url in website_urls:
                if website_url and website_url not in st.session_state.get("processed_website_urls", []):
                    with st.spinner(f"Processing Website: {website_url}"):
                        content_changed = True
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
            if content_changed and len(all_chunks) > 0:
                vectorstore = create_vectorstore(all_chunks, st.session_state.persist_directory)
                st.session_state.rag_chain = create_rag_chain(vectorstore)
                st.success("Content processed successfully! You can now ask questions.")
                content_changed = False
                st.rerun()

        except Exception as e:
            st.error(f"Error processing content: {e}")