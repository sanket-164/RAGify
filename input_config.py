import streamlit as st

def select_input():
    st.title("Input Configuration")

    st.subheader("File Types to Upload")
    st.session_state.file_extensions = st.multiselect(
        "Select file extensions for document upload",
        options=["pdf", "docx", "txt", "pptx", "xlsx"],
    )
    st.subheader("Number of YouTube Videos")
    st.session_state.no_of_yt_urls = int(st.number_input(
        "How many YouTube video URLs do you want to provide?",
        min_value=0, max_value=3, step=1
    ))

    st.subheader("Number of Website URLs")
    st.session_state.no_of_website_urls = int(st.number_input(
        "How many website URLs do you want to provide?",
        min_value=0, max_value=5, step=1
    ))

    if st.button("Start Chat"):
        st.session_state.show_sidebar = True
        st.session_state.show_balloons = True
        st.rerun()

if __name__ == "__main__":
    select_input()