/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Merges via UNION ALL writer_count era, producer_count_era, artist_count_era into one table
-- Merging via JOINs causes aggregation errors
DROP 
    TABLE IF EXISTS temp.collaborator_flat;
CREATE TABLE temp.collaborator_flat (
    era TEXT,
    collaborator TEXT,
    writer_count INTEGER,
    producer_count INTEGER,
    artist_count INTEGER,
    total_songs_writer INTEGER,
    total_songs_producer INTEGER,
    total_songs_artist INTEGER,
    total_credits INTEGER
);
INSERT INTO temp.collaborator_flat
WITH CollaboratorUnion AS (
    SELECT
        wc.era AS era1,
        'None' AS era2,
        'None' AS era3,
        wc.writer AS writer,
        'None' AS artist,
        'None' AS producer,
        wc.writer_count AS writer_count,
        0 AS producer_count,
        0 AS artist_count,
        wc.total_songs_writer AS total_songs_writer,
        0 AS total_songs_producer,
        0 AS total_songs_artist
    FROM
        writer_count_era wc
    UNION ALL
    SELECT
        'None' AS era1,
        pc.era AS era2,
        'None' AS era3,
        'None' AS writer,
        pc.producer AS producer,
        'None' AS artist,
        0 AS writer_count,
        pc.producer_count AS producer_count,
        0 AS artist_count,
        0 AS total_songs_writer,
        pc.total_songs_producer AS total_songs_producer,
        0 AS total_songs_artist
    FROM
        producer_count_era pc
    UNION ALL
    SELECT
        'None' AS era1,
        'None' AS era2,
        ac.era AS era3,
        'None' AS writer,
        'None' AS producer,
        ac.artist AS artist,
        0 AS writer_count,
        0 AS producer_count,
        ac.artist_count AS artist_count,
        0 AS total_songs_writer,
        0 AS total_songs_producer,
        ac.total_songs_artist AS total_songs_artist
    FROM
        artist_count_era ac
)
SELECT
    CASE
        WHEN era1 != 'None' THEN era1
        WHEN era2 != 'None' THEN era2
        WHEN era3 != 'None' THEN era3
    END AS era,
    CASE
        WHEN writer != 'None' THEN writer
        WHEN producer != 'None' THEN producer
        WHEN artist != 'None' THEN artist
    END AS collaborator,
    SUM(writer_count) AS writer_count,
    SUM(producer_count) AS producer_count,
    SUM(artist_count) AS artist_count,
    SUM(total_songs_writer) AS total_songs_writer,
    SUM(total_songs_producer) AS total_songs_producer,
    SUM(total_songs_artist) AS total_songs_artist,
    SUM(total_songs_writer) + SUM(total_songs_producer) + SUM(total_songs_artist) AS total_credits
FROM
    CollaboratorUnion
GROUP BY
    era, collaborator;