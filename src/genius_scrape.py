"""Functions breaking down the webbscraping process to format resulting dataframe."""

import csv
import re
from datetime import datetime

import pandas as pd
import requests
from parsel import Selector

def create_dict_from_file(csv_name):
    """Creates album dictionary from given CSV file.

       Dictionary layout: {'album_title': 'category'}, assumes
       CSV has header rows
    """
    dict = {}
    with open(csv_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dict[row['album_title']] = row['category']
    return dict

def artist_clean_name(name):
    """Formats the artist name for Genius URLs."""
    cleaned = re.sub(r'\s', '-', name)
    return cleaned

def album_clean_titles(album_list):
    """Formats album titles in given list for Genius URLs."""
    cleaned = []
    for title in album_list:
        title = re.sub(r'[^\w\s]|\s-|\'','', title)
        title = re.sub(r'\s', '-', title)
        cleaned.append(title)
    return cleaned

def album_get_tracklist(album_url):
    """Returns tracklist of given Genius album URL.

      Includes track number, song title, and link to the lyrics page
      for each song.
   """
    album_page = requests.get(album_url).text
    selector = Selector(text=album_page)
    
    number = selector.xpath(
        '//div[@class="chart_row-number_container chart_row-number_container--align_left"]/span/span/text()'
    ).getall()
    track = selector.xpath('//div[@class="chart_row-content"]/a/h3/text()').getall()
    url = selector.xpath('//div[@class="chart_row-content"]/a/@href').getall()
    clean_track = []
    
    for title in track:
        title = re.sub(r'\n|\u200b', '', title)
        title = re.sub(r'\xa0', ' ', title)
        title = title.strip()
        if title != '':
            clean_track.append(title)

    tracklist = [{'album_track_number': number,
            'song_title': title,
            'song_url': url} for number, title, url in zip(number, clean_track, url)]
    return tracklist

def song_get_artists(song_url):
    """Returns artist(s)/performer(s) of given Genius song URL.

       Also checks if there's a feature on the song; if yes, the featured
       artist/performer is included.
    """
    song_page = requests.get(song_url).text
    selector = Selector(text=song_page)

    raw_artists = selector.xpath('//div[contains(@class,"HeaderArtistAndTracklistdesktop__ListArtists")]/span/span//text()').get()
    artists = re.split(r',\s|\s&\s', raw_artists)

    feat_check = selector.xpath('//p[contains(@class,"HeaderCredits__Label")]/text()').get()

    if feat_check == 'Featuring':
        raw_feat = selector.xpath('string(//div[contains(@class, "HeaderCredits__List")])').get()
        feat = re.split(r',\s|\s&\s', raw_feat)
        artists.extend(feat)
    return artists

def song_get_metadata(song_url):
    """Returns song release date and page views of Given song URL."""
    song_page = requests.get(song_url).text
    selector = Selector(text=song_page)
    metadata = selector.xpath('//div[contains(@class,"MetadataStats__Container")]/span/span/text()').getall()

    date_check = len(metadata) >= 1 and 'viewer' not in metadata[0]
    
    if date_check == True:
        date_string = metadata[0]
        date_string = re.sub(r'[^\w\s]+','', date_string)
        date = datetime.strptime(date_string, '%b %d %Y') if len(date_string) > 4 else datetime.strptime(date_string, '%Y')
    else:
        date = None

    if len(metadata) == 3:
        views_string = metadata[2]
        views_string = views_string.split(' ')[0]
        multiplier = int
        match views_string[-1]:
            case 'M':
                multiplier = 1000000
            case 'K':
                multiplier = 1000
            case _:
                multiplier = 1
        views = int(float(views_string[0:len(views_string)-1]) * multiplier)
    else:
        views = 0
    return date, views

def song_get_lyrics(song_url):
    """Returns list of lyrics of given Genius song URL."""
    song_page = requests.get(song_url).text
    selector = Selector(text=song_page)

    raw_lyrics = selector.xpath('//div[@data-lyrics-container="true"]//text()').getall()
    lyrics_list = [re.sub(r'\u2005', ' ', lyric) for lyric in raw_lyrics]
    brackets = re.compile(r'\[.*?\]')
    lyrics = [lyric for lyric in lyrics_list if bool(brackets.match(lyric)) == False]
    return lyrics

def song_get_tags(song_url):
    """Returns genre tags of given Genius song URL."""
    song_page = requests.get(song_url).text
    selector = Selector(text=song_page)

    tags = selector.xpath('//div[@class="SongTags__Container-xixwg3-1 bZsZHM"]//text()').getall()
    return tags

def song_get_credits(song_url, credit):
    """Returns list of writers/producers of given Genius song URL.

       Variable 'credit' has to be either 'producers' or 'writers' and will
       return list of names.
    """
    if credit == 'writers':
        query = ['Writer', 'Writers']
    if credit == 'producers':
        query = ['Producer', 'Producers']
    
    song_page = requests.get(song_url).text
    selector = Selector(text=song_page)
    div_path = '//div[contains(@class,"SongInfo__Credit")]/div[preceding-sibling::div[contains(@class,"SongInfo__Label") and text()="{}"]]//text()'
    
    raw_list = selector.xpath(div_path.format(query[0])).getall()
    if raw_list == []:
        raw_list = selector.xpath(div_path.format(query[1])).getall()

    dropped = [' & ', ', ']
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
    song_metadata = [song_get_metadata(song) for song in song_urls]
    song_release_date, song_page_views = [list(field) for field in list(zip(*song_metadata))]
    song_lyrics = [song_get_lyrics(song) for song in song_urls]
    song_writers = [song_get_credits(song, 'writers') for song in song_urls]
    song_producers = [song_get_credits(song, 'producers') for song in song_urls]
    song_tags = [song_get_tags(song) for song in song_urls]

    list_index = 0

    for album in tracklists:
        for track in album:
            track.update({'song_artists':song_artists[list_index],
                          'song_release_date':song_release_date[list_index],
                          'song_page_views':song_page_views[list_index], 
                          'song_lyrics':song_lyrics[list_index], 
                          'song_writers': song_writers[list_index], 
                          'song_producers': song_producers[list_index], 
                          'song_tags': song_tags[list_index]})
            list_index += 1
        
    collection = [{'album_title': album,
                   'album_url': url,
                   'category': era,
                   'album_tracklist': list} for album, url, era, list in zip(albums, 
                                                                                   album_urls, 
                                                                                   eras, 
                                                                                   tracklists)]
    raw_df = pd.json_normalize(data=collection, record_path='album_tracklist', meta=['album_title', 
                                                                           'album_url', 
                                                                           'category'])
    
    df = raw_df.reindex(columns=['album_title', 'album_url', 'category', 'album_track_number', 'song_title', 
                                 'song_url', 'song_artists', 'song_release_date', 'song_page_views', 
                                 'song_lyrics', 'song_writers', 'song_producers', 'song_tags'])
    return df