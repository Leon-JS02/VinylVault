"""Utility functions for the analytics dashboard."""

from os import environ as ENV

from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor


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
