import pandas as pd
import requests
from parsel import Selector

def drop_songs(dataframe, song_list, remove_duplicates=True):
    """Removes rows for given songs from discography dataframe.

       By default, this function will also remove rows with duplicate
       song titles from dataframe (e.g. rereleases on EPs).
    """
    if remove_duplicates == True:
        dataframe = dataframe.drop_duplicates(subset=['song_title'])
    
    df = dataframe[~dataframe.song_title.isin(song_list)]
    return df

def add_single_song(df, album_url, album_era, song_url):
    """Adds new row to given dataframe.

       Data is collected using the given variables (album_url, album_era, and song_url),
       added to a temporary new dataframe before being concatenated to the original dataframe.
    """
    album_page = requests.get(album_url).text
    album_selector = Selector(text=album_page)

    song_page = requests.get(song_url).text
    song_selector = Selector(text=song_page)

    album_title = album_selector.xpath('//h1[contains(@class, "header_with_cover_art")]//text()').get()
    song_title = song_selector.xpath('//h1[contains(@class, "SongHeaderdesktop")]//text()').get()

    number_string = song_selector.xpath('//div[contains(@class, "HeaderArtistAndTracklist")]/text()').get()
    number = int(re.sub('\D','', number_string))

    lyrics = song_get_lyrics(song_url)
    writers = song_get_credits(song_url, 'writers')
    producers = song_get_credits(song_url, 'producers')
    tags = song_get_tags(song_url)

    new_row = [album_title, album_url, album_era, number, song_title, song_url, lyrics, writers, producers, tags]
    new_df = pd.DataFrame([new_row], columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)
    return df