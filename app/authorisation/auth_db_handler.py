"""Script to handle database interactions for the authorisation scripts."""

from os import environ as ENV
from datetime import datetime, timedelta, timezone

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


def insert_new_access_token(client_id: str, client_secret: str, access_token: str, expires_in: int):
    """Inserts a new access token into the database."""
    insert_query = """INSERT INTO access_tokens(client_id, access_token,
    client_secret, created_at, expires_at) VALUES (%s, %s, %s, %s, %s)"""

    created_at = datetime.now()
    expires_at = created_at + timedelta(seconds=expires_in)

    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(insert_query, (client_id, access_token,
                                       client_secret, created_at, expires_at))

def get_latest_token(client_id: str, client_secret: str) -> str:
    """Returns the most recent access token stored in the database."""
    stmt = """SELECT access_token FROM access_tokens
    WHERE client_id = %s AND client_secret = %s
    ORDER BY expires_at DESC
    LIMIT 1;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt, (client_id, client_secret))
            results = cur.fetchone()
    return results['access_token']

def check_token_validity(client_id: str, access_token: str) -> bool:
    """Returns true if a valid access token is available for a client id."""
    select_query = """SELECT expires_at FROM access_tokens
    WHERE client_id = %s AND access_token = %s;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(select_query, (client_id, access_token))
            results = cur.fetchone()

    if not results:
        return False

    expires_at = results['expires_at']
    return expires_at > datetime.now(timezone.utc)
