import streamlit as st
from st_pages import show_pages_from_config, add_page_title

with st.sidebar:
    show_pages_from_config()

with st.sidebar:
    with st.popover('Choose Theme'):
        select_theme = st.selectbox('Choose Theme', ('Test1', 'Test2'), label_visibility="collapsed")

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