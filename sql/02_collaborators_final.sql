/* 
The following query is written to work in a SQLite database, specifically through the sqlite3 Python module.
Depending on SQL dialect and database engine, this query may need to be modified.
*/

-- Combines collaborators with only one credit into one umbrella group
-- to save space on charts, also filters out Taylor Swift herself
WITH CollaboratorsFiltered AS (
    SELECT
        era,
        CASE
            WHEN total_credits = 1 THEN 'One-Time Collaborators'
            ELSE collaborator
        END AS collaborator,
        writer_count,
        producer_count,
        artist_count
    FROM
        collaborator_flat
    WHERE
        collaborator != 'Taylor Swift'
)
-- Aggregates writer_count, producer_count, artist_count by era, collaborator to account
-- for new umbrella group 'One-Time Collaborators', ready for pandas conversion
SELECT
    era,
    collaborator,
    SUM(writer_count) AS writer_count,
    SUM(producer_count) AS producer_count,
    SUM(artist_count) AS artist_count
FROM
    CollaboratorsFiltered
GROUP BY
    era, collaborator