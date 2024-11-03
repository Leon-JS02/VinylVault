"""Script to handle the extraction of listings from Discogs."""
import bs4
import requests

from endpoints import DISCOGS_SEARCH


def format_search_url(artist_name: str, album_name: str) -> str:
    """Formats the URL for a Discogs marketplace search for a given
    artist and album name."""
    artist_chunk = "+".join(artist_name.split(" "))
    album_chunk = "+".join(album_name.split(" "))
    filters = "&type=release&format_exact=Vinyl"
    return f"{DISCOGS_SEARCH}{artist_chunk}+{album_chunk}{filters}"
