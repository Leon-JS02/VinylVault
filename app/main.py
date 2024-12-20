"""The main endpoints for the app's front-end."""
from random import choice

from flask import Flask, request, render_template, redirect, url_for
import streamlit as st
from dotenv import load_dotenv

from extract_spotify import (search_album, parse_search_results, add_album)

from db_utils import get_album_by_id, get_all_albums, delete_album_by_id

from authorisation.access_manager import get_valid_token
from recommendation_handler import get_recommendations

app = Flask(__name__)
load_dotenv()
ACCESS_TOKEN = get_valid_token()


@app.route("/", methods=["GET"])
def index():
    """Homepage for the app."""
    return render_template("index.html"), 200


@app.route("/display_search", methods=["POST"])
def display_search():
    """Displays search results of a particular query (made through a POST request)."""
    query = request.form.get("search_query").title()
    results = search_album(query, ACCESS_TOKEN)
    parsed_results = parse_search_results(results)
    return render_template("display_search.html", albums=parsed_results, query=query)


@app.route("/add/<string:spotify_album_id>", methods=["POST"])
def add(spotify_album_id: str):
    """Adds an album of a specific Spotify ID to the user's collection."""
    add_album(spotify_album_id, ACCESS_TOKEN)
    return {"message": "Adding album to collection..."}, 200


@app.route("/delete_album", methods=["DELETE"])
def delete_album():
    """Deletes an album from the collection by its ID."""
    album_id = request.get_json()['album_id']
    delete_album_by_id(album_id)
    albums = get_all_albums()
    return render_template("collection.html", albums=albums), 200


@app.route("/collection", methods=["GET"])
def collection():
    """Displays the user's entire collection within their database."""
    albums = get_all_albums()
    return render_template("collection.html", albums=albums), 200


@app.route("/random_choice", methods=["GET"])
def random_choice():
    """Redirects the user to a random record in their collection."""
    albums = get_all_albums()
    if albums:
        random_album = choice(albums)
        random_album_id = random_album['album_id']
        return redirect(url_for('display_album', album_id=random_album_id))
    return redirect(url_for('collection'))


@app.route("/collection/<int:album_id>", methods=["GET"])
def display_album(album_id: int):
    """Displays an album of a particular ID within the user's collection."""
    # Get album by ID.
    album_info = get_album_by_id(album_id)
    return render_template("view_album.html", album=album_info), 200


@app.route("/recommend", methods=["GET"])
def recommend():
    """Gets recommendations and displays the page."""
    recs = get_recommendations(ACCESS_TOKEN)
    return render_template("recommendations.html", albums=recs)


@app.route("/analytics", methods=["GET"])
def analytics():
    """Defines the Streamlit analytics dashboard for the user's collection."""
    st.set_page_config(page_title="VinylVault - Collection Analytics")
    return {"Message": "Hello, world"}, 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.run(port=8080, debug=True)
