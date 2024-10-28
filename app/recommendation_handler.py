"""Script to handle record recommendations."""
# pylint: skip file
# skeleton

from endpoints import RECOMMENDATIONS_ENDPOINT
from db_utils import get_connection, get_cursor

def pull_artist_seeds(n: int=5) -> list[str]:
    """Pulls n random artists from the user's collection
    to seed album recommendations."""
    pass

def pull_genre_seeds(n: int=5) -> list[str]:
    """Pulls n random genres from the user's collection
    to seed album recommendations."""
    pass

def form_api_url(artist_seeds: list[str], genre_seeds: list[str]) -> str:
    """Returns a formed URL for a recommendation API call."""
    pass

def call_recommendation_endpoint(url: str, access_token: str) -> dict:
    """Calls the recommendations endpoint, returns the response."""
    pass
