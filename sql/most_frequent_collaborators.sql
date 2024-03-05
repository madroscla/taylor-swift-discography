/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Rank all collaborators by total songs worked on return most frequent
WITH collaborators_ranked AS (
    SELECT
        era,
        collaborator,
        songs,
        total_songs,
        DENSE_RANK() OVER (ORDER BY total_songs DESC) AS rank
    FROM
        collaborators_per_era
)
SELECT
    *
FROM
    collaborators_ranked
WHERE
    rank <= 9