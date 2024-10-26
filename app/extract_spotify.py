"""Script to handle the querying of the external Spotify API."""

from os import environ as ENV

import requests as req
from dotenv import load_dotenv

from endpoints import SEARCH_ENDPOINT
from authorisation.access_manager import generate_and_replace



TIMEOUT = 10


def search_album(query: str, access_token: str) -> list[dict]:
    """Returns a list of album dictionaries matching a specific search
    query from the Spotify API."""
    url = f"{SEARCH_ENDPOINT}q={query}&type=album"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = req.get(url, headers=headers, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise ConnectionError(f"Failed to retrieve data. Code: {response.status_code}")

if __name__ == "__main__":
    load_dotenv()
    generate_and_replace()
    results = search_album("ultraviolence", ENV['ACCESS_TOKEN'])
    print(results)
    