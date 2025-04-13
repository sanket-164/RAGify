import streamlit as st
from utils.constants import FILE_EXTENSION_OPTIONS, MAX_NO_OF_YOUTUBE_URL, MAX_NO_OF_WEBSITE_URL

def select_input_method():
    """
    Function to select the input method for the application.
    This function allows the user to choose the file types to upload, the number of YouTube videos,
    and the number of website URLs they want to provide.
    """

    st.title("Input Configuration")

    st.subheader("File Types to Upload")
    st.session_state.file_extensions = st.multiselect(
        "Select file extensions for document upload",
        options=FILE_EXTENSION_OPTIONS,
    )
    st.subheader("Number of YouTube Videos")
    st.session_state.no_of_yt_urls = int(st.number_input(
        "How many YouTube video URLs do you want to provide?",
        min_value=0, max_value=MAX_NO_OF_YOUTUBE_URL, step=1
    ))

    st.subheader("Number of Website URLs")
    st.session_state.no_of_website_urls = int(st.number_input(
        "How many website URLs do you want to provide?",
        min_value=0, max_value=MAX_NO_OF_WEBSITE_URL, step=1
    ))

    disable_button = False
    if st.session_state.file_extensions == [] and st.session_state.no_of_yt_urls == 0 and st.session_state.no_of_website_urls == 0:
        disable_button = True

    with st.columns(3)[1]:
        if st.button("Start Uploading", use_container_width=True, disabled=disable_button):
            upload_options = ""
            if st.session_state.file_extensions != []:
                upload_options = "Files"
            if st.session_state.no_of_yt_urls > 0:
                upload_options = "YouTube URL" if upload_options == "" else f"{upload_options}, YouTube URL"
            if st.session_state.no_of_website_urls > 0:
                upload_options = "Website URL" if upload_options == "" else f"{upload_options}, Website URL"
            st.session_state.toast_message = f"Now you can upload {upload_options} in the sidebar."
            st.session_state.show_sidebar = True
            st.session_state.show_balloons = True
            st.rerun()

if __name__ == "__main__":
    select_input_method()