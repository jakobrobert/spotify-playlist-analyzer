from flask import Flask, jsonify

import configparser

from spotify.spotify_client import SpotifyClient

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]

spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

app = Flask(__name__)


@app.route(URL_PREFIX + "hello-world", methods=["GET"])
def index():
    response = {"message": "<h1>Hello World!</h1>"}
    return jsonify(response)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    # TODO LATER: apply sorting & filters. for now, keep in client

    return jsonify(playlist)
