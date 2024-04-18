/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Summarizes songs counts by release formats
SELECT
    classification,
    COUNT(*) AS total_songs
FROM
    release_info
GROUP BY
    classification;