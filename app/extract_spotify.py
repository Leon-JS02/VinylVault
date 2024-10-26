"""Script to handle the querying of the external Spotify API."""

from os import environ as ENV
from datetime import datetime
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
        return response.json()["albums"]["items"]
    raise ConnectionError(f"Failed to retrieve data. Code: {response.status_code}")

def parse_release_date(release_date: str, release_date_precision: str) -> str:
    """Returns a standardised release date string in
      dd/mm/yyyy format from a string and a precision value."""
    if release_date_precision not in ["day", "month", "year"]:
        raise ValueError("Invalid date precision given.")
    if release_date_precision == "year":
        date_obj = datetime.strptime(release_date, "%Y")
        return date_obj.strftime("01/01/%Y")
    if release_date_precision == "month":
        date_obj = datetime.strptime(release_date, "%Y-%m")
        return date_obj.strftime("01/%m/%Y")

    date_obj = datetime.strptime(release_date, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")

def parse_artists(album: dict) -> str:
    """Returns a string of comma joined artists from a Spotify album dict."""
    artists = [x['name'] for x in album.get("artists",[])]
    return ",".join(artists)

def get_image_url(album: dict) -> str:
    """Returns the URL for an album's art from a dict."""
    images = [x['url'] for x in album['images']]
    return images[0] if images else None
    

def parse_search_results(albums: list[dict]) -> list[dict]:
    """Strips unnecessary information from the album dictionaries.
    Returns a list of cleaned album dictionary objects."""
    return[
        {
            "title": x['name'],
            "release_date": parse_release_date(x['release_date'], x['release_date_precision']),
            "artist": parse_artists(x),
            "spotify_id": x['id'],
            "img_url": get_image_url(x),
        }
        for x in albums
    ]