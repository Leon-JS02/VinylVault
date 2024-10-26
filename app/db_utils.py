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