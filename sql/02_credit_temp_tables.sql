/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Temp table of amount of writing credits per person per era, includes overall total per person
DROP 
    TABLE IF EXISTS temp.writer_count_era;
CREATE TABLE temp.writer_count_era (
    era TEXT,
    writer TEXT,
    writer_count INTEGER,
    total_songs_writer INTEGER
);
INSERT INTO temp.writer_count_era 
SELECT 
    a.album_era AS era,
    w.song_writer AS writer,
    COUNT(*) AS writer_count,
    SUM(COUNT(*)) OVER (PARTITION BY w.song_writer) AS total_songs_writer
FROM 
    albums a
    LEFT JOIN songs s ON a.album_title = s.album_title
    LEFT JOIN writers w ON s.song_title = w.song_title
GROUP BY
    a.album_era, w.song_writer;

-- Temp table of amount of producing credits per person per era, includes overall total per person
DROP 
    TABLE IF EXISTS temp.producer_count_era;
CREATE TABLE temp.producer_count_era (
    era TEXT,
    producer TEXT,
    producer_count INTEGER,
    total_songs_producer INTEGER
);
INSERT INTO temp.producer_count_era 
SELECT 
    a.album_era AS era,
    p.song_producer AS producer,
    COUNT(*) AS producer_count,
    SUM(COUNT(*)) OVER (PARTITION BY p.song_producer) AS total_songs_producer
FROM 
    albums a
    LEFT JOIN songs s ON a.album_title = s.album_title
    LEFT JOIN producers p ON s.song_title = p.song_title
GROUP BY
    a.album_era, p.song_producer;

-- Temp table of amount of artist/performing credits per person per era, includes overall total per person
DROP 
    TABLE IF EXISTS temp.artist_count_era;
CREATE TABLE temp.artist_count_era (
    era TEXT,
    artist TEXT,
    artist_count INTEGER,
    total_songs_artist INTEGER
);
INSERT INTO temp.artist_count_era 
SELECT 
    a.album_era AS era,
    sa.song_artist AS artist,
    COUNT(*) AS artist_count,
    SUM(COUNT(*)) OVER (PARTITION BY sa.song_artist) AS total_songs_artist
FROM 
    albums a
    LEFT JOIN songs s ON a.album_title = s.album_title
    LEFT JOIN artists sa ON s.song_title = sa.song_title
GROUP BY
    a.album_era, sa.song_artist;