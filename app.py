import streamlit as st
from input_config import select_input_method
from sidebar import sidebar
from session import session_initialization
from chat import load_chat_history, handle_user_prompt

# Main function to run the Streamlit app
def main():
    
    st.title("RAGify")

    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False
    
    if st.session_state.toast_message:
        st.toast(st.session_state.toast_message)
        st.session_state.toast_message = ""
    
    load_chat_history()

    if st.session_state.show_sidebar:
        st.markdown(
            """
            <style>
                .stMainBlockContainer{
                    width: 70%;
                    max-width: 100%;
                    padding-top : 2rem;
                    padding-left : 0rem;
                    padding-right : 0rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        sidebar()
    else:
        select_input_method()

    # User input for chat
    if st.session_state.rag_chain is not None:
        if prompt := st.chat_input("Ask a question about the content..."):
            handle_user_prompt(prompt)
                

if __name__ == "__main__":
    session_initialization()
    main()