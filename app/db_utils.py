"""Script to handle the database interactions for the main app."""

from os import environ as ENV

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection, cursor
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> connection:
    """Returns a database connection."""
    return connect(
        dbname=ENV['DB_NAME'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        host=ENV['DB_HOST'],
        port=ENV['DB_PORT']
    )


def get_cursor(conn: connection) -> cursor:
    """Returns a database cursor for a connection."""
    return conn.cursor(cursor_factory=RealDictCursor)


def insert_artist(spotify_artist_id: str, artist_name: str) -> int:
    """Inserts an artist into the database, returning its ID."""
    stmt = """INSERT INTO artist(spotify_artist_id, artist_name)
    VALUES (%s, %s) RETURNING artist_id;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (spotify_artist_id, artist_name,))
            artist_id = cur.fetchone()['artist_id']
        conn.commit()
    return artist_id


def insert_genre(genre_name: str) -> int:
    """Inserts an genre into the database, returning its ID."""
    stmt = """INSERT INTO genre(genre_name)
    VALUES (%s) RETURNING genre_id;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (genre_name,))
            genre_id = cur.fetchone()['genre_id']
        conn.commit()
    return genre_id


def insert_artist_genre_assignment(artist_id: int, genre_id: int):
    """Inserts an artist genre assignment into the database."""
    stmt = """INSERT INTO artist_genre_assignment(artist_id, genre_id)
    VALUES (%s, %s);"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (artist_id, genre_id,))
        conn.commit()


def insert_album(album_info: tuple) -> int:
    """Inserts an album into the database, returning its ID."""
    (artist_id, spotify_album_id, album_type, album_name,
     release_date, num_tracks, runtime_seconds, art_url) = album_info
    stmt = """INSERT INTO album(artist_id, spotify_album_id, album_type,
    album_name, release_date, num_tracks, runtime_seconds, album_art_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING album_id;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (artist_id, spotify_album_id, album_type,
                               album_name, release_date, num_tracks, runtime_seconds, art_url,))
            album_id = cur.fetchone()['album_id']
        conn.commit()
    return album_id


def get_all_albums() -> list[dict]:
    """Retrieves a list of all albums from the user's collection."""
    stmt = """SELECT ar.artist_name, a.* FROM
    artist AS ar JOIN album AS a USING (artist_id);"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt)
            res = cur.fetchall()
    return [
        {
            'album_id': x['album_id'],
            'title': x['album_name'],
            'artist': x['artist_name'],
            'release_date': x['release_date'],
            'img_url': x['album_art_url']
        } for x in res]


def get_all_artists() -> dict:
    """Returns a dict of all Spotify artist IDs in the database."""
    stmt = "SELECT artist_id, spotify_artist_id FROM artist;"
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt)
            results = cur.fetchall()
    return {x['spotify_artist_id']: x['artist_id'] for x in results}


def get_all_genres() -> dict:
    """Returns a dict of all genres mapped to their IDs."""
    stmt = "SELECT genre_id, genre_name FROM genre;"
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt)
            res = cur.fetchall()
    return {x['genre_name']: x['genre_id'] for x in res}


def get_album_by_id(album_id: int) -> dict:
    """Retrieves full details of an album from the database by a specific ID."""
    stmt = """SELECT ar.artist_name, a.*, 
    STRING_AGG(g.genre_name, ', ' ORDER BY g.genre_name ASC) 
    AS genres FROM genre AS g JOIN artist_genre_assignment 
    USING(genre_id) JOIN album AS a USING(artist_id) 
    JOIN artist AS ar USING(artist_id) WHERE album_id = %s
    GROUP BY a.album_id, ar.artist_name;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (album_id,))
            res = cur.fetchone()

    return {
        "title": res['album_name'],
        "artist": res['artist_name'],
        "genres": res['genres'],
        "release_date": res['release_date'],
        "num_tracks": res['num_tracks'],
        "runtime_seconds": res['runtime_seconds'],
        "album_art_url": res['album_art_url']
    }
