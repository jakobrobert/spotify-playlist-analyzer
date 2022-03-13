from flask import Flask, render_template, request, redirect, url_for

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


@app.route(URL_PREFIX + "playlist-by-url", methods=["GET"])
def get_playlist_by_url():
    playlist_url = request.args.get("playlist_url")

    playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
    redirect_url = url_for("get_playlist_by_id",
                           playlist_id=playlist_id, sort_by="none", ascending_or_descending="ascending")

    return redirect(redirect_url)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    sort_by = request.args.get("sort_by")
    ascending_or_descending = request.args.get("ascending_or_descending")

    songs = spotify_client.get_songs_of_playlist(playlist_id)
    __sort_songs(songs, sort_by, ascending_or_descending)

    return render_template("playlist.html",
                           songs=songs, playlist_id=playlist_id,
                           sort_by=sort_by, ascending_or_descending=ascending_or_descending)


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]


def __sort_songs(songs, sort_by, ascending_or_descending):
    if sort_by == "none":
        return

    reverse = (ascending_or_descending == "descending")
    songs.sort(key=lambda song: song[sort_by], reverse=reverse)
