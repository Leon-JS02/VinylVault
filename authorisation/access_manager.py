"""Script to handle the Spotify access tokens used for authorisation."""

import requests as req

TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

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