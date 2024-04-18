/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Summarizes page views by era
SELECT
    era,
    SUM(views) as total_views
FROM
    song_views
GROUP BY
    era;