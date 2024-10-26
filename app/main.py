"""The main endpoints for the app's front-end."""

from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Homepage for the app."""
    return {"message": "VinylVault Search"}, 200


@app.route("/display_search", methods=["POST"])
def display_search():
    """Displays search results of a particular query (made through a POST request)."""
    return {"message": "Displaying search results..."}, 200


@app.route("/add/<str:spotify_album_id>", methods=["POST"])
def add(spotify_album_id: str):
    """Adds an album of a specific Spotify ID to the user's collection."""
    return {"message": "Adding album to collection..."}, 200

@app.route("/collection", methods=["GET"])
def collection():
    """Displays the user's entire collection within their database."""
    return {"message": "Displaying all albums in collection..."}, 200


@app.route("/collection/<int:album_id>", methods=["GET"])
def display_album(album_id: int):
    """Displays an album of a particular ID within the user's collection."""
    return {"message": "Displaying the chosen album..."}, 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8080, debug=True)
