"""Script to handle the Spotify access tokens used for authorisation."""

from os import environ as ENV

import requests as req

from authorisation.auth_db_handler import get_latest_token, check_token_validity, insert_new_access_token

TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
REQUIRED_AUTH_KEYS = ["CLIENT_ID", "CLIENT_SECRET"]


def call_token_api(client_id: str, client_secret: str) -> str:
    """Calls the Spotify token API and returns an authorisation token."""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = req.post(TOKEN_ENDPOINT, headers=headers, data=data, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data.get("access_token"), data.get("expires_in")

    raise ConnectionError("Error. Please check your credentials.")

def get_valid_token() -> str:
    """Returns the latest token if still valid. Else generates, stores, and returns
    a new token."""
    if not all(key in ENV for key in REQUIRED_AUTH_KEYS):
        raise ValueError(".env has not been configured correctly.")
    latest_token = get_latest_token(ENV['CLIENT_ID'], ENV['CLIENT_SECRET'])
    if check_token_validity(ENV['CLIENT_ID'], latest_token):
        return latest_token
    new_token, expires_in = call_token_api(ENV['CLIENT_ID'], ENV['CLIENT_SECRET'])
    insert_new_access_token(ENV['CLIENT_ID'], ENV['CLIENT_SECRET'], new_token, expires_in)
    return new_token

