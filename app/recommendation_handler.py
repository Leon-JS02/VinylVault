"""Script to handle record recommendations."""

import requests as req

from endpoints import RECOMMENDATIONS_ENDPOINT
from db_utils import get_connection, get_cursor


def pull_artist_seeds(n: int = 3) -> list[str]:
    """Pulls n random artists from the user's collection
    to seed album recommendations."""
    stmt = """SELECT spotify_artist_id
    FROM artist ORDER BY RANDOM();"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt)
            results = cur.fetchall()
    return [x['spotify_artist_id'] for x in results[:n]]


def pull_genre_seeds(n: int = 2) -> list[str]:
    """Pulls n random genres from the user's collection
    to seed album recommendations."""
    stmt = """SELECT genre_name
    FROM genre ORDER BY RANDOM();"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(stmt)
            results = cur.fetchall()
    return [x['genre_name'] for x in results[:n]]


def form_api_url(artist_seeds: list[str], genre_seeds: list[str]) -> str:
    """Returns a formed URL for a recommendation API call."""
    artist_chunk = "%2C".join(artist_seeds)
    genre_chunk = "%2C".join(genre_seeds)
    url = f"{RECOMMENDATIONS_ENDPOINT}seed_artists={artist_chunk}&seed_genres={genre_chunk}"
    return url


def call_recommendation_endpoint(url: str, access_token: str) -> dict:
    """Calls the recommendations endpoint, returns the response."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = req.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise ConnectionError(
            f"Failed to call recommendation API. Code: {response.status_code}")
    return response.json()


def parse_recommendations(recs_dict: dict) -> list[dict]:
    """Returns a list of album objects from the recommendations JSON response."""
    parsed = []
    for rec in recs_dict['tracks']:
        parsed.append(
            {
                'album_name': rec['album']['name'],
                'artist_name': ", ".join(x['name'] for x in rec['artists']),
                'release_date': rec['album']['release_date'],
                'img_url': rec['album']['images'][0]['url']
            }
        )
    return parsed


def get_recommendations(access_token: str) -> list[dict]:
    """The main function for the recommendation handler.
    Calls the recommendations endpoint and returns a list 
    of parsed album objects."""
    artist_seeds = pull_artist_seeds()
    genre_seeds = pull_genre_seeds()
    url = form_api_url(artist_seeds, genre_seeds)
    recs = call_recommendation_endpoint(url, access_token)
    return parse_recommendations(recs)
