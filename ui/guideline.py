import streamlit as st

def general_instructions():
    st.markdown(f"""
    ### 🧠 Chat Guidelines
    - The chatbot **only knows what you’ve uploaded or linked** – no general web search.
    - Keep follow-up questions **related to your provided content**.
    - **Be specific**, Ask about particular sections or topics for better answers.
    - Use **clear and concise language** to improve response accuracy.
    - If the bot doesn't understand, **rephrase your question**.
    - **Avoid** asking about unrelated topics or general knowledge.

    ### 📤 Uploading Files
    - Make sure uploaded documents do have texts to be extracted. 
    - File names must be unique.
    - You can upload **multiple files** at once.

    ### 📺 YouTube URLs
    - Only paste valid **full YouTube links** starting with `http`.
    - The audio will be transcribed and summarized automatically.

    ### 🌐 Website URLs
    - URLs must start with `http://` or `https://`.
    - Avoid login-protected pages or dynamic JavaScript-heavy content.
    """, unsafe_allow_html=True)

    if st.button("Go Back & Edit Input", use_container_width=True):
        st.session_state.show_sidebar = False
        st.rerun()
