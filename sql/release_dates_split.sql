/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Table of release dates split into separate columns
SELECT
    song_title,
    release_year AS year,
    release_month AS month,
    release_day AS day
FROM
    release_info;