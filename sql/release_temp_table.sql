/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Temp table of release classifications and broken down release dates
-- Used throughout "Release Overview" app page
DROP 
    TABLE IF EXISTS temp.release_info;
CREATE TABLE temp.release_info (
    era TEXT,
    song_title TEXT,
    classification TEXT,
    release_month INTEGER,
    release_day INTEGER,
    release_year INTEGER
);
INSERT INTO temp.release_info
SELECT
    a.category AS era,
    s.song_title AS song_title,
    CASE
        WHEN a.category IN ("Fearless (TV)", "Red (TV)", "Speak Now (TV)", "1989 (TV)") THEN "Rerecorded Albums"
        WHEN a.category = "Other Artist Songs" THEN "Other Artists' Albums"
        WHEN a.category = "Non-Album Songs" THEN "Other Release Formats"
        ELSE "Studio Albums"
    END AS classification,
    strftime('%m', s.song_release_date) AS release_month,
    strftime('%d', s.song_release_date) AS release_day,
    strftime('%Y', s.song_release_date) AS release_year
FROM
    songs s
    LEFT JOIN albums a ON s.album_title = a.album_title;