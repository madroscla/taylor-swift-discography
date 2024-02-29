"""Additional functions for modifying discography dataframe.

   (Not to be confused with Discogs, the online music database.)
"""

import csv
import re

import pandas as pd
import requests
import sqlite3 as sql
from parsel import Selector

from src import genius_scrape

def drop_song(df, song_name, drop_duplicates=True):
    """Removes rows for given songs from discography dataframe.

       By default, this function will also remove rows with duplicate
       song titles from dataframe (e.g. rereleases on EPs).
    """
    if drop_duplicates == True:
        df = df.drop_duplicates(subset=['song_title'])
    
    df = df[df['song_title'] != song_name]
    return df

def drop_songs_from_file(df, csv_name, drop_duplicates=True):
    """Drops multiple songs at once from given CSV file.

       By default, this function will also remove rows with duplicate
       song titles from dataframe (e.g. rereleases on EPs).
    """
    if drop_duplicates == True:
        df = df.drop_duplicates(subset=['song_title'])
        
    with open('data/csv/{}'.format(csv_name), 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            song_title = row['song_title']
            df = drop_song(df, song_title, False)
    return df

def add_song(df, album_url, category, song_url):
    """Adds new song to discography dataframe.

       Data is collected using the given variables (album_url, category, and song_url),
       added to a temporary new dataframe before being concatenated to the original. This is
       also used to add songs without albums (e.g. promo singles).
    """
    album_checker = True if album_url == '' else False
    album_url_checker = 'NA' if album_checker == True else album_url
    
    album_page = 'NA' if album_checker == True else requests.get(album_url).text
    album_selector = 'NA' if album_checker == True else Selector(text=album_page)

    song_page = requests.get(song_url).text
    song_selector = Selector(text=song_page)

    album_title = 'NA' if album_url == '' else album_selector.xpath('//h1[contains(@class, "header_with_cover_art")]//text()').get()
    song_title = song_selector.xpath('//h1[contains(@class, "SongHeaderdesktop")]//text()').get()

    number_string = 'NA' if album_checker == True else song_selector.xpath('//div[contains(@class, "HeaderArtistAndTracklist")]/text()').get()
    number = 0 if album_checker == True else int(re.sub('\D','', number_string))

    artists = genius_scrape.song_get_artists(song_url)
    release_date, page_views = genius_scrape.song_get_metadata(song_url)
    lyrics = genius_scrape.song_get_lyrics(song_url)
    writers = genius_scrape.song_get_credits(song_url, 'writers')
    producers = genius_scrape.song_get_credits(song_url, 'producers')
    tags = genius_scrape.song_get_tags(song_url)

    new_row = [album_title, album_url_checker, category, number, song_title, song_url, artists, release_date, page_views, lyrics, writers, producers, tags]
    new_df = pd.DataFrame([new_row], columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)
    return df

def add_songs_from_file(df, csv_name):
    """Adds multiple songs at once from given CSV file."""
    with open('data/csv/{}'.format(csv_name), 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            album_url = row['album_url']
            category = row['category']
            song_url = row['song_url']
            df = add_song(df, album_url, category, song_url)
    return df

def change_credit_name(series, old_name, new_name):
    """Changes name of individual in song credits.

       Can only be done in song_artists, song_writers, or song_producers
       since this function assumes a list value in series.
    """
    series = series.apply(lambda list: [new_name if string == old_name else string for string in list])
    return series

def convert_to_db(df, db_name):
    """Converts discography dataframe to a SQLite database.

       By default makes six tables (albums, songs, artists, writers,
       producers, tags), replacing them if they already exist.
    """
    connection = sql.connect('data/{}'.format(db_name))

    albums = df[['album_title','album_url', 'category']].drop_duplicates(subset=['album_title','album_url'])
    albums.reset_index(inplace=True, drop=True)
    albums.to_sql('albums', connection, if_exists='replace')
    
    songs = df[['song_title','album_title', 'album_track_number', 'song_url', 'song_release_date', 'song_page_views', 'song_lyrics']]
    songs.reset_index(inplace=True, drop=True)
    songs.to_sql('songs', connection, if_exists='replace')

    artists = df[['song_title', 'song_artists']].explode(['song_artists'])
    artists.rename(columns={'song_artists': 'song_artist'}, inplace=True)
    artists.reset_index(inplace=True, drop=True)
    artists.to_sql('artists', connection, if_exists='replace')
    
    writers = df[['song_title', 'song_writers']].explode(['song_writers'])
    writers.rename(columns={'song_writers': 'song_writer'}, inplace=True)
    writers.reset_index(inplace=True, drop=True)
    writers.to_sql('writers', connection, if_exists='replace')
    
    producers = df[['song_title', 'song_producers']].explode(['song_producers'])
    producers.rename(columns={'song_producers': 'song_producer'}, inplace=True)
    producers.reset_index(inplace=True, drop=True)
    producers.to_sql('producers', connection, if_exists='replace')
    
    tags = df[['song_title', 'song_tags']].explode(['song_tags'])
    tags.rename(columns={'song_tags': 'song_tag'}, inplace=True)
    tags.reset_index(inplace=True, drop=True)
    tags.to_sql('tags', connection, if_exists='replace')
    connection.close()