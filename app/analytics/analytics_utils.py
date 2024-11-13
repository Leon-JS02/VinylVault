"""Utility functions for the analytics dashboard."""

from os import environ as ENV

from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor

from queries import decade_counts, genre_counts, tag_counts, album_count


def get_connection() -> connection:
    """Returns a live database connection."""
    return connect(
        database=ENV['DB_NAME'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=ENV['DB_PORT'],
        host=ENV['DB_HOST']
    )


def get_cursor(conn: connection) -> cursor:
    """Returns a RealDictCursor from a database connection."""
    return conn.cursor(cursor_factory=RealDictCursor)


def execute_query(query: str) -> list[dict]:
    """Executes a given SQL query and returns its results set."""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(query)
            res = cur.fetchall()
    return res


def get_decade_counts() -> dict[str, int]:
    """Returns a dictionary mapping decade to number of releases."""
    results = execute_query(decade_counts)
    return {
        str(row['decade_name']): row['decade_count']
        for row in results
    }


def get_genre_counts() -> dict[str, int]:
    """Returns a dictionary mapping genre to number of releases."""
    results = execute_query(genre_counts)
    return {
        row['genre_name']: row['genre_count']
        for row in results
    }


def get_tag_counts() -> dict[str, int]:
    """Returns a dictionary mapping tag to number of releases."""
    results = execute_query(tag_counts)
    return {
        row['tag_name']: row['tag_count']
        for row in results
    }


def get_album_count() -> int:
    """Returns the number of releases in the user's collection."""
    results = execute_query(album_count)
    return results[0]['count']
