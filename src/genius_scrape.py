"""Functions breaking down the webbscraping process to format resulting dataframe."""

import csv
import re

import pandas as pd
import requests
from parsel import Selector

def create_dict_from_file(csv_name):
    """Creates album dictionary from given CSV file.

       Dictionary layout: {'album_title': 'album_era'}, assumes
       CSV has header rows
    """
    dict = {}
    with open('data/csv/{}'.format(csv_name), 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dict[row['album_title']] = row['album_era']
    return dict

def artist_clean_name(name):
    """Formats the artist name for Genius URLs."""
    cleaned = re.sub('\s', '-', name)
    return cleaned

def album_clean_titles(album_list):
    """Formats album titles in given list for Genius URLs."""
    cleaned = []
    for title in album_list:
        title = re.sub('[^\w\s]|\s-|\'','', title)
        title = re.sub('\s', '-', title)
        cleaned.append(title)
    return cleaned

def album_get_tracklist(url):
    """Returns tracklist of given Genius album URL.

      Includes track number, song title, and link to the lyrics page
      for each song.
   """
    album_page = requests.get(url).text
    selector = Selector(text=album_page)
    
    number = selector.xpath(
        '//div[@class="chart_row-number_container chart_row-number_container--align_left"]/span/span/text()'
    ).getall()
    track = selector.xpath('//div[@class="chart_row-content"]/a/h3/text()').getall()
    url = selector.xpath('//div[@class="chart_row-content"]/a/@href').getall()
    clean_track = []
    
    for title in track:
        title = re.sub('\n|\u200b', '', title)
        title = re.sub('\xa0', ' ', title)
        title = title.strip()
        if title != '':
            clean_track.append(title)

    tracklist = [{'album_track_number': number,
            'song_title': title,
            'song_url': url} for number, title, url in zip(number, clean_track, url)]
    return tracklist

def song_get_artists(url):
    """Returns artist(s)/performer(s) of given Genius song URL.

       Also checks if there's a feature on the song; if yes, the featured
       artist/performer is included.
    """
    song_page = requests.get(url).text
    selector = Selector(text=song_page)

    raw_artists = selector.xpath('//div[@class="HeaderArtistAndTracklistdesktop__Container-sc-4vdeb8-0 hjExsS"]/span/span//text()').get()
    artists = re.split(',\s|\s&\s', raw_artists)

    feat_check = selector.xpath('//p[contains(@class,"HeaderCredits__Label")]/text()').get()

    if feat_check == 'Featuring':
        raw_feat = selector.xpath('string(//div[contains(@class, "HeaderCredits__List")])').get()
        feat = re.split(',\s|\s&\s', raw_feat)
        artists.extend(feat)
    return artists

def song_get_lyrics(url):
    """Returns lyrics of given Genius song URL."""
    song_page = requests.get(url).text
    selector = Selector(text=song_page)

    raw_lyrics = selector.xpath('//div[@data-lyrics-container="true"]//text()').getall()
    lyrics_list = [re.sub('\u2005', ' ', lyric) for lyric in raw_lyrics]
    lyrics = ' '.join(lyrics_list)
    lyrics = re.sub('\[.*?\]', '', lyrics)
    lyrics = re.sub('\s\s', ' ', lyrics)
    lyrics = re.sub('\(\s', '(', lyrics)
    lyrics = re.sub('\s\)', ')', lyrics)
    lyrics = re.sub('^\s', '', lyrics)
    return lyrics

def song_get_tags(url):
    """Returns genre tags of given Genius song URL."""
    song_page = requests.get(url).text
    selector = Selector(text=song_page)

    tags = selector.xpath('//div[@class="SongTags__Container-xixwg3-1 bZsZHM"]//text()').getall()
    return tags

def song_get_credits(url, credit):
    """Returns list of writers/producers of given Genius song URL.

       Variable 'credit' has to be either 'producers' or 'writers' and will
       return list of names.
    """
    if credit == 'writers':
        query = 'Written By'
    elif credit == 'producers':
        query = 'Produced By'
    
    song_page = requests.get(url).text
    selector = Selector(text=song_page)
    raw_list = selector.xpath(
        '//div[@class="SongInfo__Credit-nekw6x-3 fognin" and contains(., "{}")]//text()'.format(query)
    ).getall()
    
    dropped = ['Written By', 'Produced By', ' & ', ', ']
    credits = [name for name in raw_list if name not in dropped]
    return credits

def create_discography(artist, albums_dict):
    """Compiles all webscraping data into one discography dataframe."""
    albums = list(albums_dict.keys())
    eras = list(albums_dict.values())
    cleaned_albums = album_clean_titles(albums)
    cleaned_artist = artist_clean_name(artist)
    album_urls = ['https://genius.com/albums/{}/{}'.format(cleaned_artist, title) for title in cleaned_albums]

    tracklists = [album_get_tracklist(url) for url in album_urls]

    song_urls = [track['song_url'] for list in tracklists for track in list]

    song_artists = [song_get_artists(song) for song in song_urls]
    song_lyrics = [song_get_lyrics(song) for song in song_urls]
    song_writers = [song_get_credits(song, 'writers') for song in song_urls]
    song_producers = [song_get_credits(song, 'producers') for song in song_urls]
    song_tags = [song_get_tags(song) for song in song_urls]

    list_index = 0

    for album in tracklists:
        for track in album:
            track.update({'song_artists':song_artists[list_index], 
                          'song_lyrics':song_lyrics[list_index], 
                          'song_writers': song_writers[list_index], 
                          'song_producers': song_producers[list_index], 
                          'song_tags': song_tags[list_index]})
            list_index += 1
        
    collection = [{'album_title': album,
                   'album_url': url,
                   'album_era': era,
                   'album_tracklist': list} for album, url, era, list in zip(albums, 
                                                                                   album_urls, 
                                                                                   eras, 
                                                                                   tracklists)]
    raw_df = pd.json_normalize(data=collection, record_path='album_tracklist', meta=['album_title', 
                                                                           'album_url', 
                                                                           'album_era'])
    
    df = raw_df.reindex(columns=['album_title', 'album_url', 'album_era', 'album_track_number', 'song_title', 
                                 'song_url', 'song_artists', 'song_lyrics', 'song_writers', 'song_producers', 'song_tags'])
    return df