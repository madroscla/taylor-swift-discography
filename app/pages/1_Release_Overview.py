import os
import sys
from datetime import date

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
        section.main > div {max-width:65rem}
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

today = date(2024, 5, 5)
today_format = today.strftime("%B %-d, %Y")

def main():
    sidebar()
    content()

def sidebar():
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')
        st.markdown("""
        <h3 style="text-align: center;">Taylor Swift - Song Discography</h3>

        <p style="text-align: center;">This is an ongoing, open-source project. Follow along on <a href='https://github.com/madroscla/taylor-swift-discography'>Github</a>!</p>

        <p style="text-align: center;">Data was last updated on <b>{}</b>.</p>
        
        """.format(today_format), unsafe_allow_html=True)

@st.cache_data
def content():
    st.markdown("""
    ## Song Release Formats

    Taylor Swift currently has over 350 songs in her discography: many have been released on her studio albums, but a significant amount have been released in other formats. To better visualize her discography, I categorized her songs into four groups based on release format: songs on her studio albums (including deluxe versions), songs on her rerecorded albums, songs on other artists' albums (not including soundtracks), and any miscellanious release formats such as EPs, promotional singles, or soundtrack releases.
    """)
    
    release_formats = toolkit.sql_to_string('release_formats.sql')
    
    formats = pd.read_sql(release_formats, connection)
    formats_table = formats.set_index('classification')

    formats_fig, formats_ax = charts.formats_pie(custom_params, formats, 'total_songs', 'classification', 'Song Release Formats', 
                                             ['#f6fff8', '#eaf4f4', '#cce3de', '#a4c3b2'], True, 'release_formats.png', True, formats)
    
    st.pyplot(formats_fig)

    with st.expander("See discussion"):
        st.write("""
            From this pie chart, we can clearly see that songs released on studio albums make up the vast majority of Taylor's discography, accounting for over 59%. Interestingly, nearly a third of her discography includes the rerecorded versions of her earlier songs, despite only beginning her rerecording process in the past five years. Contributions on other artists' studio albums and miscellanious releases only make up a small percentage of her discography, being just udner 13% combined.
            """)

    st.markdown("""
    ## Song Release Dates

    With a nearly 18-year-long career, Taylor Swift often releases music around the same times of year and even on the same days as previous releases. Since the start of the 2020s and the beginning of her rerecording process, her releases-per-year have been much higher than they have in the past. To see overall patterns in the release dates, I visualize two metrics:

    1. I plot the frequency distributions for release years, release months, and release days independently, seeing which years, months and days respectively Taylor has released most of her music.
    2. I plot release months against release days to find the most common dates on which Taylor tends to release music.
    """)
    release_dates_split = toolkit.sql_to_string('release_dates_split.sql')
    releases = pd.read_sql(release_dates_split, connection)

    releases_fig, releases_ax = charts.release_hist(custom_params, releases, 'year', 'month', 'day', 'Frequency Distributions of Song Release Dates', 
                                             'Release Years', 'Release Months', 'Release Days', 'Year', 'Month', 'Day of Month', 'Song Count', 
                                             ['#d00000', '#e85d04', '#faa307'], ['#6a040f'], True, 'release_dates_distribution.png')
    st.pyplot(releases_fig)

    with st.expander("See discussion"):
        st.write("""
            In terms of her most productive years, Taylor has released most of her music between 2019 and 2024. This range makes sense, as Taylor not only released two studio albums in 2020, but began her rerecording process, releasing two rerecorded albums both in 2021 and 2023. Outside of this range, her most productive year was 2012 with the release of her studio album "Red," along with some non-album releases like her contributions to The Hunger Games' movie soundtrack. Her least productive year was 2015, with only one song being released, followed by a three-way tie between 2013, 2016, and 2018. All three of these years were between studio album releases, with Taylor usually touring internationally, so it's not surprising to see these years have limited releases. Still, it's interesting to compare these touring years with her constant productivity in 2023 and 2024, despite being on the Eras Tour.

            For productive months, Taylor tends to release her songs in October, with nearly a third of her entire catalogue being released then. Other months of high activity are November, April, and July, having 60, 59, and 41 songs releases respectively. She does not often release music in February, June, or January, the former only having 3 song releases and the latter two each having 5 song releases. Taylor also tends to release songs later in the month, most being released between the 19th and 27th days of the month. She also tends to release songs on the 12th, 7th, 9th, and 11th days of the month, falling within the first two weeks of a month.
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
            The previously noticed pattern of releasing in October still appears when plotting release months against release days, with three different dates in October being in the top 10 most frequent release dates: 10/21, 10/22, and 10/27, the last of which has the most number of song releases. The other months that had high releease distributions when independently plotted show up in the top 10 as well: 4/9 and 4/19 for April, 7/7 and 7/24 for July, and 11/12 for November. These release dates also match the pattern of Taylor either releasing music between the 19th and 27th dates of the month or within the first two weeks of the month.
            """)

if __name__ == '__main__':
    main()

connection.close()