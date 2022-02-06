from flask import Flask, render_template, request

import configparser
import requests

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")


@app.route(URL_PREFIX + "songs-of-playlist", methods=["GET"])
def get_songs_of_playlist():
    playlist_url = request.args.get("playlist_url")
    print(f"playlist_url: {playlist_url}")

    # TODO this is just a test token, replace by proper Authentication flow
    access_token = "BQBPTOQbOcNgbylEde97_eMLX4AilcQxnEMP0WuaDvmex_5CeGUW3IwCECcQ4xCtze3xsgdh9UPyEMzu5u9XxXkweHTTm1wjBTd97IGQBJa8zIBdEpbU3N7hVU2ZQ2Z8Mha0JSCu40YRUrveFb-ScFXn17KeWyjbgnI "
    playlist_id = "2cE4QPx8FAtUIOsZpHwAQM"  # TODO currently hardcoded, get playlist id based on the playlist url
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    response_json = response.json()
    print(f"response_json: {response_json}")

    songs = []

    # TODO use data of response
    """
    for i in range(0, 10):
        song = {"artist": f"Artist {i}", "title": f"Title {i}"}
        songs.append(song)
    """

    return render_template("songs_of_playlist.html", songs=songs, num_songs=len(songs))
