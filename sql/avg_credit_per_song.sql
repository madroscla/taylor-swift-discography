/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Calculate average number of writers/prodcuers/artists per song per era
SELECT
    era,
    "writer" AS type,
    ROUND(
        CAST(total_writers AS REAL) / total_songs,
        2
    ) AS avg_per_song
FROM
    credit_counts_per_era
UNION
SELECT
    era,
    "producer" AS type,
    ROUND(
        CAST(total_producers AS REAL) / total_songs,
        2
    ) AS avg_per_song
FROM
    credit_counts_per_era
UNION
SELECT
    era,
    "artist" AS type,
    ROUND(
        CAST(total_artists AS REAL) / total_songs,
        2
    ) AS avg_per_song
FROM
    credit_counts_per_era;