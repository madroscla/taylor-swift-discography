import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import streamlit as st

st.set_page_config(page_title="About the Data")

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

        <p style="text-align: center;">This is an ongoing, open-source project. Follow along on <a href='https://github.com/madroscla/taylor-swift-discography'>Github</a>!
        
        """, unsafe_allow_html=True)

@st.cache_data
def content():
    st.markdown("""
    ## About the Data

    All data for this project has been scraped from Genius using the Python package [parsel](https://parsel.readthedocs.io/en/latest/). The data is then formatted into a SQLite database, from which all the data in this application is queried. The database has the following format:
    """)

    st.image('figures/db_schema.png')

    st.markdown("""    
    Please check out [this notebook on the project's Github](https://github.com/madroscla/taylor-swift-discography/blob/main/notebooks/data_collection.ipynb) for more details on the data was scraped. 
    """)

    st.markdown("""
    ## Data Preview

    The database used in this application as well as the pickle versions of the data can be found on the [project's Github](https://github.com/madroscla/taylor-swift-discography/tree/main/data). The data is also available in CSV format on [Kaggle](https://www.kaggle.com/datasets/madroscla/taylor-swift-released-song-discography-genius) for public use under the CC BY-SA 4.0 license.
    """)

    df = pd.read_pickle('data/taylor_swift_clean.pkl')

    st.dataframe(df.sample(100))
    st.markdown("""
    ## Constraints and Limitations of Discography
    
    This discography prioritizes *song* coverage over *album* coverage; this means that deluxe versions of albums with more songs are preferred over standard versions, and that album releases are preferred over single/EP releases. While not all versions of a song's release will be covered in this dataset, it contains every unique song. Rerecorded songs count as separate entries from their original versions.
    
    Please see table below for more information on what is and isn't included in the discography:
    
    | Included in Discography | Not Included in Discography |
    | -- | -- |
    | Songs released on Taylor Swift studio albums  | Duplicate song entries (e.g. for single release, album release, deluxe album release, etc.) |
    | Songs released on Taylor Swift rerecorded "Taylor's Version" albums | Unreleased/leaked songs and demos |
    | Songs by Taylor Swift for soundtracks or released as non-album singles | Covers of Taylor Swift songs by other artists |
    | Remixes of Taylor Swift songs featuring new performing artists | Remixes/acoustic versions of songs not featuring new performing artists|
    | Songs written by Taylor Swift for other artists, even if they don't feature Taylor | Live versions of songs/song mashups previously accounted for |
    | Songs by other artists featuring Taylor Swift | Songs that sample/interpolate Taylor Swift songs, even if they list her as a writer or feature |
    | Song covers by or featuring Taylor Swift that have been officially recorded and released | Songs that only exist in video format (DVD, live show recording, etc.) |
    """)

if __name__ == '__main__':
    main()