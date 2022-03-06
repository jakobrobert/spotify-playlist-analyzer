from flask import Flask, render_template, request

import configparser

from spotify.spotify_client import SpotifyClient

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]

spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")


@app.route(URL_PREFIX + "songs-of-playlist", methods=["GET"])
def get_songs_of_playlist():
    playlist_url = request.args.get("playlist_url")
    playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
    songs = spotify_client.get_songs_of_playlist(playlist_id)

    # TODO clean up: num_songs is obsolete, can use len(songs) in jinja code?
    return render_template("songs_of_playlist.html", songs=songs, num_songs=len(songs))


@app.route(URL_PREFIX + "sort-songs", methods=["GET"])
def sort_songs():
    print(f"request data: {request.args}")
    #print(f"len(songs): {len(songs)}")


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]
