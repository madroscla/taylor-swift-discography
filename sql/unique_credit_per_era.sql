/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Restructures unique_credits_per_era for visualization
SELECT
    era,
    "writer" AS type,
    unique_writers AS unique_count
FROM
    unique_credits_per_era
UNION
SELECT
    era,
    "producer" AS type,
    unique_producers AS unique_count
FROM
    unique_credits_per_era
UNION
SELECT
    era,
    "artist" AS type,
    unique_artists AS unique_count

FROM
    unique_credits_per_era;