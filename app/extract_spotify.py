"""Script to handle the querying of the external Spotify API."""

from datetime import datetime

import requests as req

from endpoints import SEARCH_ENDPOINT, ARTIST_ENDPOINT, ALBUM_ENDPOINT
from db_utils import (insert_artist, insert_genre, insert_artist_genre_assignment,
                      insert_album, get_all_artists, get_all_genres)


TIMEOUT = 10


def search_album(query: str, access_token: str) -> list[dict]:
    """Returns a list of album dictionaries matching a specific search
    query from the Spotify API."""
    url = f"{SEARCH_ENDPOINT}q={query}&type=album"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = req.get(url, headers=headers, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.json()["albums"]["items"]
    raise ConnectionError(
        f"Failed to retrieve data. Code: {response.status_code}:{access_token}")


def call_get_artist_endpoint(artist_id: str, access_token: str) -> dict:
    """Makes an API call to the artist_id endpoint. Returns the response dict."""
    url = f"{ARTIST_ENDPOINT}{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = req.get(url, headers=headers, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise ConnectionError(
        f"Failed to retrieve data. Code: {response.status_code}")


def call_get_album_endpoint(album_id: str, access_token: str) -> dict:
    """Makes an API call to the artist_id endpoint. Returns the response dict."""
    url = f"{ALBUM_ENDPOINT}{album_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = req.get(url, headers=headers, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise ConnectionError(
        f"Failed to retrieve data. Code: {response.status_code}")


def parse_artist_from_api(response: dict) -> dict:
    """Removes unnecessary details from a get artist API response."""
    return {
        'spotify_id': response['id'],
        'name': response['name'],
        'genres': response['genres']
    }


def calculate_runtime(tracks: dict) -> int:
    """Calculates the runtime of an album from a tracks dict."""
    items = tracks.get('items', [])
    return round(sum(x.get('duration_ms', 0) for x in items)/1000)


def parse_album_from_api(response: dict) -> dict:
    """Removes unnecessary details from a get album API response."""
    return {
        'num_tracks': response['total_tracks'],
        'album_type': response['album_type'],
        'artists': [{
            'spotify_id': x['id'],
            'name': x['name']
        } for x in response['artists']],
        'runtime_seconds': calculate_runtime(response['tracks']),
        'title': response['name'],
        'release_date': parse_release_date(response['release_date'],
                                           response['release_date_precision']),
        'art_url': get_image_url(response)
    }


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
    return date_obj.strftime("%Y-%m-%d")


def parse_artists(album: dict) -> str:
    """Returns a string of comma joined artists from a Spotify album dict."""
    artists = [x['name'] for x in album.get("artists", [])]
    return ", ".join(artists)


def get_image_url(album: dict) -> str:
    """Returns the URL for an album's art from a dict."""
    images = [x['url'] for x in album['images']]
    return images[0] if images else None


def get_artists_from_artist_ids(artist_ids: list, access_token: str) -> list[dict]:
    """Returns a list of artist dicts from an album ID."""
    responses = [call_get_artist_endpoint(x, access_token) for x in artist_ids]
    return [parse_artist_from_api(response) for response in responses]


def parse_search_results(albums: list[dict]) -> list[dict]:
    """Strips unnecessary information from the album dictionaries.
    Returns a list of cleaned album dictionary objects."""
    return [
        {
            "title": x['name'],
            "release_date": parse_release_date(x['release_date'], x['release_date_precision']),
            "artist": parse_artists(x),
            "spotify_id": x['id'],
            "img_url": get_image_url(x),
        }
        for x in albums
    ]


def add_album(spotify_album_id: str, access_token: str):
    """Adds an album to the database, handling foreign key dependencies."""
    album_data = fetch_and_parse_album_data(spotify_album_id, access_token)
    artist_ids = process_artists(album_data['artists'], access_token)
    primary_artist_id = artist_ids[0]
    album_info = (
        primary_artist_id, spotify_album_id, album_data['album_type'],
        album_data['title'], album_data['release_date'],
        album_data['num_tracks'], album_data['runtime_seconds'],
        album_data['art_url']
    )
    insert_album(album_info)


def fetch_and_parse_album_data(spotify_album_id: str, access_token: str) -> dict:
    """Fetches album data from the API and parses it."""
    response = call_get_album_endpoint(spotify_album_id, access_token)
    return parse_album_from_api(response)


def process_artists(artists: list, access_token: str) -> list:
    """Processes and inserts artists if necessary, returning their IDs."""
    artist_ids = []
    all_artists = get_all_artists()
    all_genres = get_all_genres()

    for artist in artists:
        artist_id = get_or_create_artist(
            artist, all_artists, all_genres, access_token)
        artist_ids.append(artist_id)

    return artist_ids


def get_or_create_artist(artist: dict, all_artists: dict,
                         all_genres: dict, access_token: str) -> int:
    """Retrieves or inserts an artist and their genres."""
    spotify_id = artist['spotify_id']

    if spotify_id not in all_artists:
        artist_id = insert_artist(spotify_id, artist['name'])
        all_artists[spotify_id] = artist_id
        fetch_and_assign_genres(artist_id, spotify_id,
                                all_genres, access_token)
    else:
        artist_id = all_artists[spotify_id]

    return artist_id


def fetch_and_assign_genres(artist_id: int, spotify_id: str, all_genres: dict, access_token: str):
    """Fetches and assigns genres to an artist, inserting any new genres."""
    artist_info = parse_artist_from_api(
        call_get_artist_endpoint(spotify_id, access_token))

    for genre in artist_info.get('genres', []):
        if genre not in all_genres:
            genre_id = insert_genre(genre)
            all_genres[genre] = genre_id
        else:
            genre_id = all_genres[genre]

        insert_artist_genre_assignment(artist_id, genre_id)

