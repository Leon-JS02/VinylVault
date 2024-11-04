# pylint: skip-file

tag_counts = """
SELECT t.tag_name, COUNT(t.tag_id) AS tag_count
FROM tag AS t
JOIN album_tag_assignment
AS ata ON ata.tag_id = t.tag_id
GROUP BY t.tag_name
ORDER BY tag_count DESC;
"""

genre_counts = """
SELECT g.genre_name, COUNT(g.genre_id) AS genre_count
FROM genre AS g
JOIN artist_genre_assignment
AS aga ON aga.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY genre_count DESC;
"""

decade_counts = """
WITH AlbumDecades AS (
    SELECT a.album_name, 
           FLOOR(EXTRACT(YEAR FROM a.release_date) 
           / 10) * 10 AS decade_name
    FROM album AS a
)
SELECT ad.decade_name, COUNT(ad.decade_name) AS decade_count
FROM AlbumDecades AS ad
GROUP BY ad.decade_name
ORDER BY decade_count DESC;
"""

album_count = """
SELECT COUNT(*) FROM album;
"""
