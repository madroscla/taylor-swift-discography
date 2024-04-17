/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Counts number of songs released for each month/day combo
SELECT
    release_month AS month,
    release_day AS day,
    CAST(release_month AS TEXT) || "/" || CAST(release_day AS TEXT) AS date,
    COUNT(*) AS count
FROM
    release_info
GROUP BY
    release_month, release_day;