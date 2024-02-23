import pandas as pd
import sqlite3 as sql

def convert_to_db(dataframe, db_name):
    """Converts discography dataframe to a SQLite database.

       By default makes five tables (albums, songs, writers, producers, 
       tags), replacing them if they already exist.
    """
    connection = sql.connect('data/{}'.format(db_name))

    albums = dataframe[['album_title','album_url', 'album_era']].drop_duplicates(subset=['album_title','album_url'])
    albums.reset_index(inplace=True, drop=True)
    albums.to_sql('albums', connection, if_exists='replace')
    
    songs = dataframe[['song_title','album_title', 'album_track_number', 'song_url', 'song_lyrics']]
    songs.reset_index(inplace=True, drop=True)
    songs.to_sql('songs', connection, if_exists='replace')

    artists = dataframe[['song_title', 'song_artists']].explode(['song_artists'])
    artists.rename(columns={'song_artists': 'song_artist'}, inplace=True)
    artists.reset_index(inplace=True, drop=True)
    artists.to_sql('artists', connection, if_exists='replace')
    
    writers = dataframe[['song_title', 'song_writers']].explode(['song_writers'])
    writers.rename(columns={'song_writers': 'song_writer'}, inplace=True)
    writers.reset_index(inplace=True, drop=True)
    writers.to_sql('writers', connection, if_exists='replace')
    
    producers = dataframe[['song_title', 'song_producers']].explode(['song_producers'])
    producers.rename(columns={'song_producers': 'song_producer'}, inplace=True)
    producers.reset_index(inplace=True, drop=True)
    producers.to_sql('producers', connection, if_exists='replace')
    
    tags = dataframe[['song_title', 'song_tags']].explode(['song_tags'])
    tags.rename(columns={'song_tags': 'song_tag'}, inplace=True)
    tags.reset_index(inplace=True, drop=True)
    tags.to_sql('tags', connection, if_exists='replace')
    connection.close()