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

