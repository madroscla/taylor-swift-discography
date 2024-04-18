/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Temp table of songs, their categories, and their page views
-- Used throughout "Genius Page Views" app page
DROP 
    TABLE IF EXISTS temp.song_views;
CREATE TABLE temp.song_views (
    era TEXT,
    song_title TEXT,
    views INTEGER
);
INSERT INTO temp.song_views
SELECT
    a.category AS era,
    s.song_title AS song_title,
    s.song_page_views AS views
FROM
    albums a
    LEFT JOIN songs s ON a.album_title = s.album_title;