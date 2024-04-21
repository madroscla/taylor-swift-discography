import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st

st.markdown(
    """
    <style>
        section.main > div {max-width:75rem}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    sidebar()
    content()

def sidebar():
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')
        st.markdown("""
        <h3 style="text-align: center;">Taylor Swift - Song Discography</h3>

        <p style="text-align: center;">This is an ongoing, open-source project. Follow along on <a href='https://github.com/madroscla/taylor-swift-discography'>Github</a>!</p>

        <p style="text-align: center;">Data was last updated on <b>April 21, 2024</b>.</p>
        
        """, unsafe_allow_html=True)

def content():
    st.image('assets/img/TTPDLogo.png')
    st.markdown(
        """
    # Welcome!

    This application represents an ongoing project to compile and analyze Taylor Swift's song discography as it exists on [Genius](https://genius.com/). Here you will find several different exploratory data analyses of different aspects of Taylor Swift's songs, including how and when they're released, who she creates her music with, and the traffic for each song on Genius. As Taylor releases more music, this application will grow, with immediate plans for analysis of her lyrics using NLP.

    This project is completely open-source, not for profit, and free for public use; I only ask that you link back here and give credit!

    * Follow along with the project on [Github](https://github.com/madroscla/taylor-swift-discography)
    * Add the developer (me) on [LinkedIn](https://www.linkedin.com/in/madelinerclark/) or check out [my personal website](https://madelinerclark.com/)
    """
    )

if __name__ == '__main__':
    main()
