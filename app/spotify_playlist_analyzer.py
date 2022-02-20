from flask import Flask, render_template, request

import configparser
import requests
import datetime

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")


@app.route(URL_PREFIX + "songs-of-playlist", methods=["GET"])
def get_songs_of_playlist():
    playlist_url = request.args.get("playlist_url")
    playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
    access_token = __get_spotify_access_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response_data = response.json()

    tracks = response_data["tracks"]["items"]

    songs = []

    for track in tracks:
        track_item = track["track"]

        title = track_item["name"]
        artists = __get_artists_of_track(track_item)
        duration = __get_duration_of_track(track_item)
        release_date = __get_release_date_of_track(track_item)

        song = {"artists": artists, "title": title, "duration": duration, "release_date": release_date}
        songs.append(song)

    return render_template("songs_of_playlist.html", songs=songs, num_songs=len(songs))


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]


def __get_spotify_access_token():
    url = "https://accounts.spotify.com/api/token"
    grant_type = "client_credentials"
    data = {"grant_type": grant_type}
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    response = requests.post(url, data=data, auth=auth)
    response_data = response.json()

    return response_data["access_token"]


def __get_artists_of_track(track):
    artists_string = ""
    artists = track["artists"]

    for i in range(len(artists)):
        artist_name = artists[i]["name"]
        if i != 0:
            artists_string += ", "
        artists_string += artist_name

    return artists_string


def __get_duration_of_track(track):
    milliseconds = track["duration_ms"]
    total_seconds = milliseconds // 1000
    total_minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60

    return f"{total_minutes:02d}:{remaining_seconds:02d}"


def __get_release_date_of_track(track):
    album = track["album"]
    release_date = album["release_date"]

    return release_date

