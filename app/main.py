"""The main endpoints for the app's front-end."""
from os import environ as ENV

from flask import Flask, request
from dotenv import load_dotenv

from extract_spotify import (search_album, parse_search_results, add_album,
                             call_get_album_endpoint, parse_album_from_api)
from db_utils import get_album_by_id
from authorisation.access_manager import generate_and_replace

app = Flask(__name__)
load_dotenv()


@app.route("/", methods=["GET"])
def index():
    """Homepage for the app."""
    return {"message": "VinylVault Search"}, 200


@app.route("/display_search", methods=["POST"])
def display_search():
    """Displays search results of a particular query (made through a POST request)."""
    query = request.form.get("search_query")
    print(query)
    results = search_album(query, ENV['ACCESS_TOKEN'])
    parsed_results = parse_search_results(results)
    return parsed_results, 200


@app.route("/add/<string:spotify_album_id>", methods=["POST"])
def add(spotify_album_id: str):
    """Adds an album of a specific Spotify ID to the user's collection."""
    add_album(spotify_album_id, ENV['ACCESS_TOKEN'])
    return {"message": "Adding album to collection..."}, 200


@app.route("/collection", methods=["GET"])
def collection():
    """Displays the user's entire collection within their database."""
    return {"message": "Displaying all albums in collection..."}, 200


@app.route("/collection/<int:album_id>", methods=["GET"])
def display_album(album_id: int):
    """Displays an album of a particular ID within the user's collection."""
    # Get album by ID.
    album_info = get_album_by_id(album_id)
    return {}, 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8080, debug=True)
