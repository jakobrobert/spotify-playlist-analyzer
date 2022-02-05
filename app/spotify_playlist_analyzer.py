from flask import Flask, render_template, request

import configparser

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

    # TODO get data of this playlist using Spotify Web API

    songs = []
    for i in range(0, 10):
        song = {"artist": f"Artist {i}", "title": f"Title {i}"}
        songs.append(song)

    return render_template("songs_of_playlist.html", songs=songs)
