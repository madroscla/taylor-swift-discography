import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st

def main():
    sidebar()
    content()

def sidebar():
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')
        st.markdown("""
        <h3 style="text-align: center;">Taylor Swift - Song Discography</h3>

        This is an open source project that is still ongoing.
        
        """, unsafe_allow_html=True)


def content():
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
            forums](https://discuss.streamlit.io)
    """
    )

if __name__ == '__main__':
    main()
