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
    return artist_id


def insert_genre(genre_name: str) -> int:
    """Inserts an genre into the database, returning its ID."""
    stmt = """INSERT INTO genre(genre_name)
    VALUES (%s) RETURNING genre_id;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (genre_name,))
            genre_id = cur.fetchone()['genre_id']
    return genre_id
