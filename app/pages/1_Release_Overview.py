import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import streamlit as st
import sqlite3 as sql
from matplotlib import rcParams

from src import charts
from src import toolkit

st.set_page_config(page_title="Release Overview")

st.markdown(
    """
    <style>
        section.main > div {max-width:75rem}
    </style>
    """,
    unsafe_allow_html=True
)

connection = sql.connect('data/taylor_swift.db')
cursor = connection.cursor()

rcParams, custom_params = toolkit.chart_params(rcParams)

# Creating temporary table to be used throughout
temp_table = toolkit.sql_to_string('release_temp_table.sql')
cursor.executescript(temp_table)

def main():
    content()

def content():
    release_formats = toolkit.sql_to_string('release_formats.sql')
    
    formats = pd.read_sql(release_formats, connection)
    formats_table = formats.set_index('classification')

    formats_fig, formats_ax = charts.formats_pie(custom_params, formats, 'total_songs', 'classification', 'Song Release Formats', 
                                                 ['#f6fff8', '#eaf4f4', '#cce3de', '#a4c3b2'], True, 'release_formats.png', True, formats_table)
    
    st.pyplot(formats_fig)

    with st.expander("See discussion"):
        st.write("""
            test
            """)

    release_dates_split = toolkit.sql_to_string('release_dates_split.sql')
    releases = pd.read_sql(release_dates_split, connection)

    releases_fig, releases_ax = charts.release_hist(custom_params, releases, 'year', 'month', 'day', 'Frequency Distributions of Song Release Dates', 
                                             'Release Years', 'Release Months', 'Release Days', 'Year', 'Month', 'Day of Month', 'Song Count', 
                                             ['#d00000', '#e85d04', '#faa307'], ['#6a040f'], True, 'release_dates_distribution.png')
    st.pyplot(releases_fig)

    with st.expander("See discussion"):
        st.write("""
            test
            """)

    month_day_distribution = toolkit.sql_to_string('month_day_distribution.sql')
    month_day = pd.read_sql(month_day_distribution, connection)
    dates = month_day.sort_values(by=['count'], ascending=False)
    dates = dates[['date', 'count']].head(10)

    freq_dates_fig, freq_dates_ax = charts.date_scatter(custom_params, month_day, 'month', 'day', 'count', 'Most Frequent Release Dates', 
                                                        'Month', 'Day of Month', True, 'most_frequent_dates.png', True, dates)
    st.pyplot(freq_dates_fig)

    with st.expander("See discussion"):
        st.write("""
            test
            """)

if __name__ == '__main__':
    main()

connection.close()