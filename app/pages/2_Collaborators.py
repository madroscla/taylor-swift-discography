import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import streamlit as st
import sqlite3 as sql
from matplotlib import rcParams

from src import charts
from src import toolkit

st.set_page_config(page_title="Collaborators")

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

eras = ['Taylor Swift',
        'Fearless',
        'Speak Now',
        'Red',
        '1989',
        'reputation',
        'Lover',
        'folklore',
        'evermore',
        'Fearless (TV)',
        'Red (TV)',
        'Midnights',
        'Speak Now (TV)',
        '1989 (TV)',
        'Non-Album Songs',
        'Other Artist Songs']

credits = {
    'writer': '#6D466B',
    'producer': '#58A4B0',
    'artist': '#FF6B6C'}

rcParams, custom_params = toolkit.chart_params(rcParams)

# Creating several temporary tables to be used throughout
temp_tables = toolkit.sql_to_string('collab_temp_tables.sql')
cursor.executescript(temp_tables)

def main():
    sidebar()
    content()

def sidebar():
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')

@st.cache_data
def content():
    st.markdown("""
    ## Most Collaborative Eras
    
    Over her career, Taylor Swift has worked with numerous writers, producers, and fellow artists to create her musical catalogue, demonstrated by the musician credits on each song. However, some of her albums and overall musical eras are more collaborative efforts than others; while an album may not have many featured artists, it could still be very collaborative in terms of writing or producing. In order to see which eras had overall more collaborators than others, I use two approaches:
    
    1. I count the number of *unique* writers, producers, and artists per song and summarize by era. I then calculate the means for each musician type across all eras. Finally, I compare the totals per era to the means to determine which eras are the most and least collaborative.
    2. I count the *total* number of writers, producers, and artists per song before summarizing by era. I then calculate the average amount of writers, producers, and artists per song for each era, as well as the overall means for each musician type per song. Finally, I compare the eras' averages to the overall means to determine which eras are the most and least collaborative.
    """)
    
    st.markdown("""### Unique Musicians Per Era""")
    
    unique_credit_per_era = toolkit.sql_to_string('unique_credit_per_era.sql')
    
    unique_credit = pd.read_sql(unique_credit_per_era, connection)
    toolkit.sort_cat_column(unique_credit, 'era', eras)
    
    # Pivoting dataframe for chart table
    unique_credit_pivot = unique_credit.pivot(columns='era', index='type', values='unique_count')
    unique_credit_pivot.sort_values('type', ascending=False, inplace=True)
    
    # Calculating overall means for type
    avg_per_type_unique = unique_credit.groupby('type')['unique_count'].mean().sort_values(ascending=False)
    
    credits_total_fig, credits_total_ax = charts.credit_chart(credits, custom_params, 'bar', unique_credit, 'era', 'unique_count', 'type', 
                        avg_per_type_unique, 'Total Unique Musicial Credits Per Era',
                        'Album/Song Era', '# Per Era (Count)', 'Credit Type', True,
                        True, 'unique_credits_per_era.png', True, unique_credit_pivot)
    st.pyplot(credits_total_fig)
    
    with st.expander("See discussion"):
        st.write("""
            Looking at the bars, we can clearly see which eras had the most unique collaborators. More than any album or rerecording, Taylor works with the more unique musicians when collaborating on other artists' songs or when creating non-album songs, as the former's totals for producers and artists and the latter's total for writers are higher than any other era. Following those two is "Red (Taylor's Version)," which has the second highest total for each artists and third highest for both producers and writers. For the lowest totals, "Speak Now (Taylor's Version)" only has 1 unique writer for the era, "Fearless" has only 2 unique producers, and the debut "Taylor Swift" only has 1 unique artist.
            
            To determine her most and least collaborative eras, we'll look at where the totals fall relative the overall means per type (represented by horizontal dash lines). For her most collaborative eras, both her collaborations on other artist's songs and her non-album works fall above the means for all three musician types; "Red (Taylor's Version)" also has totals above all three means, being her only studio album or rerecording to do so. For least collaborative, several eras fall below the overall means for all three types: the self-titled "Taylor Swift," "Fearless," "Speak Now," "folklore," "evermore," and "Speak Now (Taylor's Version)." This makes it difficult to narrow down which albums could be considered the least collaborative.
            
            I also have other issues with determinining collaborativeness through this approach: one issue is that it doesn't take into consideration the lengths of albums and how that can skew the counts of unique musicians. For instance, "Red (Taylor's Version)" has over 30 songs associated with the era, while "folklore" and "evermore" only have 17 each; even if "folklore" and "evermore" featured unique writers, producers, and/or artists for every track, it's still possible for them to fall below "Red (Taylor's Version)" in totals due to having less songs overall. Also, this method doesn't account for variability between individual songs when it comes to writers, producers, or artists. For example, "Midnights" features a track, "Lavender Haze," that has 6 unique writers alone while also featuring a track, "Bigger Than the Whole Sky," that is solely written by Taylor herself. That variation is not accounted for when totaling unique writers between the two tracks, which would still be a total of 6.
            
            Accounting for these issues lead me to my second approach: calculating the average musician type per indiviudal song and comparing the overall averages by era.
        """)
        
    st.markdown("""### Average Musicians Per Song By Era""")
    
    avg_credit_per_song = toolkit.sql_to_string('avg_credit_per_song.sql')
    
    avg_credit = pd.read_sql(avg_credit_per_song, connection)
    toolkit.sort_cat_column(avg_credit, 'era', eras)
    
    # Pivoting dataframe for chart table
    avg_credit_pivot = avg_credit.pivot(columns='era', index='type', values='avg_per_song')
    avg_credit_pivot.sort_values('type', ascending=False, inplace=True)
    
    # Calculating overall means for type-per-song
    avg_per_type = avg_credit.groupby('type')['avg_per_song'].mean().sort_values(ascending=False)
    
    avg_credits_fig, avg_credits_ax = charts.credit_chart(credits, custom_params, 'line', avg_credit, 'era', 'avg_per_song', 'type', 
                        avg_per_type, 'Average Number of Musicial Credits Per Song By Era',
                        'Album/Song Era', '# Per Song (Average)', 'Credit Type', True,
                        True, 'avg_credits_per_song.png', True, avg_credit_pivot)
    st.pyplot(avg_credits_fig)
    
    with st.expander("See discussion"):
        st.write("""
            This analytical approach gives us a more nuanced way to which eras were more collaborative in terms of individual musician types. For instance, both "reputation" and "Midnights" were highly collaborative eras, with the former having the highest average of writers per song (3.13 writers) and the latter having the highest average of producers per song (2.46 producers). Meanwhile, both "Speak Now" and "Speak Now (Taylor's Version)" have the lowest average of 1.11 and 1.0 writers per song respectively, the rerecording being solely written by Taylor herself, and the self-titled "Taylor Swift" has the lowest average of 1.14 producers per song, followed by "evermore" at 1.41 producers. Her collaborations with artists tend to be more steady, many albums having few vocal features, but "Red (Taylor's Version)" boasts the highest average of her studio albums and rerecordings, of 1.22 artists per song. Unsurprisingly, this is surpassed by her collaboration songs on other artists' albums, which have an average artist-per-song of 1.87 and usually feature another artist alongside Taylor Swift.
            
            To determine her most and least collaborative eras, we'll once again look at where the average values fall relative the overall means (represented by horizontal dash lines). Three eras fall below all three means: "Speak Now", "Red", and "folklore." That means that, according to both this approach and the previous approach, "Speak Now" and "folklore" are considered Taylor's least collaborative eras. Interestingly, no era has all values fall above the overall means; "Lover" has higher averages for both writers-per-song and producers-per-song, but its average for artists-per-song is equal to the overall mean for artists-per-song. Regardless, its values being at-or-above each mean makes it the most collaborative era via this approach, despite not being considered especially collaborative via the previous approach.
            
            Whichever method one uses to determine most and least collaborative eras is ultimately up to the individual. While both of these approaches determine collaborativeness in their own ways, I can only conclude which eras are Taylor Swift's least collaborative ("Speak Now" and "folklore") based on the results of these two approaches.
            """)
    
    st.markdown("""
    ## Most Frequent Collaborators
    
    Even in some of her least collaborative eras, Taylor Swift has several musicians that she works regularly with to create her music. I want to see which musicians Taylor collaborates with the most, but my methodology needs to be adjusted. Many of her regular cowriters also help produce her songs, meaning that if we were to just count their music credits, we could accidentally double-count a musician for one song. Instead, I count how many songs they worked on per era, regardless of whether they wrote the song, produced it, sang it, or some combination of the three.
    
    For sake of brevity, I rank each of Taylor's collaborators on the total number of songs they worked on across her discography, with #1 having the most songs worked on, and select the twelve musicians with the highest ranks (I would have selected ten, but there's a four-way tie and I want to include them all).
    """)
    
    most_frequent_collabs = toolkit.sql_to_string('most_frequent_collaborators.sql')
    
    freq_collabs = pd.read_sql(most_frequent_collabs, connection)
    toolkit.sort_cat_column(freq_collabs, 'era', eras)
    
    collab_totals = freq_collabs.loc[:,('collaborator', 'total_songs')]
    collab_totals.drop_duplicates('collaborator', inplace=True)
    collab_totals.sort_values('collaborator', inplace=True)
    collab_totals.set_index('collaborator', inplace=True)
    
    freq_collabs_fig, freq_collabs_ax = charts.collab_heatmap(custom_params, freq_collabs, 'era', 'collaborator', 'songs', 'sum', 
                   'Most Frequent Collaborators Per Era', 'Album/Song Era', 'Collaborator Name', 
                   True, True, 'most_frequent_collabs_per_era.png', table_bool=True, table_df=collab_totals)
    st.pyplot(freq_collabs_fig)
    
    with st.expander("See discussion"):
        st.write("""
            From this heatmap, we can see in which eras Taylor's most frequent collaborators worked on the most songs. Jack Antonoff has the clear lead, collaborating on a total of 72 songs across Taylor's discography, with 21 songs alone being from "Midnights." We can also see at what point Jack began to work with Taylor; his first collaborations were during "1989" and he has since been a mainstay in every studio album and rerecording.
            
            Meanwhile, the #2 collaborator, Nathan Chapman, stops working with Taylor shortly after she transitions from country to pop music, only working on 1 song during "1989" despite being credited several times on her previous albums. Interestingly, he does not return to produce the songs on the rerecorded versions of "Fearless," "Speak Now" and "Red." This is despite several collaborators from the original albums coming back for the rerecorded versions, like Liz Rose for "Fearless (Taylor's Version)" and Max Martin and Shellback for "1989 (Taylor's Version)." Instead, Christopher Rowe, Taylor's #3 collaborator, seems to step in to do the bulk of the rerecording collaborations, despite not having worked with Taylor prior to "Fearless (Taylor's Version)."
            """)

if __name__ == '__main__':
    main()

connection.close()