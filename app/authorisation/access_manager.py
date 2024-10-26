"""Script to handle the Spotify access tokens used for authorisation."""

from os import environ as ENV

import requests as req
from dotenv import set_key

from auth_db_handler import insert_new_access_token, check_token_validity

TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
REQUIRED_AUTH_KEYS = ["CLIENT_ID", "CLIENT_SECRET", "ACCESS_TOKEN"]


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


def overwrite_dotenv(auth_token: str) -> None:
    """Overwrites the value for 'ACCESS_TOKEN' in the .env"""
    set_key(ENV['ENV_PATH'], "ACCESS_TOKEN", auth_token)


def setup_authentication() -> str:
    """Initialises the authentication for use within the main app.
    Checks for a valid access token, client ID, and client secret.
    Reauthenticates if necessary. Returns a valid token."""
    if not all(key in ENV for key in REQUIRED_AUTH_KEYS):
        raise ValueError(".env has not been configured correctly.")
    # User must be reauthenticated - expired token
    if not check_token_validity(ENV['CLIENT_ID'], ENV['ACCESS_TOKEN']):
        generate_and_replace()
    return ENV['ACCESS_TOKEN']


def generate_and_replace():
    """Main function for the script. Generates and replaces
    the old access token within the .env file."""
    auth_token, expires_in = call_token_api(
        ENV['CLIENT_ID'], ENV['CLIENT_SECRET'])
    overwrite_dotenv(auth_token)
    insert_new_access_token(
        ENV['CLIENT_ID'], ENV['CLIENT_SECRET'], auth_token, expires_in)


if __name__ == "__main__":
    generate_and_replace()
