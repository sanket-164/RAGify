import streamlit as st

from ui.sidebar import sidebar
from ui.guideline import general_instructions
from ui.input_config import select_input_method
from ui.chat import load_chat_history, handle_user_prompt

from utils.session import session_initialization


st.set_page_config(
    page_title="RAGify",
    page_icon="images/RAGify-Logo.png",
    layout="wide",
    menu_items=None,
)

def main():

    col1, col2 = st.columns([0.5, 5])  # Adjust ratio as needed

    with col1:
        st.image("images/RAGify-Logo.png", use_container_width=True)

    with col2:
        st.title("RAGify")


    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False
    
    if st.session_state.toast_message:
        st.toast(st.session_state.toast_message)
        st.session_state.toast_message = ""

    if st.session_state.show_sidebar:
        st.markdown(
            """
            <style>
                .stMainBlockContainer{
                    width: 70%;
                    max-width: 100%;
                    padding-top : 5rem;
                    padding-left : 0rem;
                    padding-right : 0rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        sidebar()
        if st.session_state.messages == []:
            general_instructions()
        else:
            load_chat_history()
        
        # User input for chat
        if st.session_state.rag_chain is not None:
            if prompt := st.chat_input("Ask a question about the content..."):
                handle_user_prompt(prompt)
    else:
        st.markdown(
                """
                <style>
                    .stMainBlockContainer {
                        width: 50%;
                        max-width: 100%;
                        padding-top : 5rem;
                        padding-left : 0rem;
                        padding-right : 0rem;
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )
        select_input_method()

if __name__ == "__main__":
    session_initialization()
    main()