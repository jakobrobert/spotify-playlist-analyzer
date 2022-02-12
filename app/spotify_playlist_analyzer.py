from flask import Flask, render_template, request

import configparser
import requests

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

    playlist_id_start_index = playlist_url.find("playlist/") + len("playlist/")
    playlist_id_end_index = playlist_url.find("?")
    playlist_id = playlist_url[playlist_id_start_index:playlist_id_end_index]

    access_token = __get_spotify_access_token()

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    response = requests.get(url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    response_data = response.json()
    tracks = response_data["tracks"]["items"]

    songs = []

    for track in tracks:
        track_item = track["track"]

        title = track_item["name"]

        artists = track_item["artists"]
        artists_string = ""
        for i in range(len(artists)):
            artist_name = artists[i]["name"]
            if i != 0:
                artists_string += ", "
            artists_string += artist_name

        song = {"artists": artists_string, "title": title}
        songs.append(song)

    return render_template("songs_of_playlist.html", songs=songs, num_songs=len(songs))


def __get_spotify_access_token():
    url = "https://accounts.spotify.com/api/token"
    grant_type = "client_credentials"
    data = {"grant_type": grant_type}
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    response = requests.post(url, data=data, auth=auth)
    response_data = response.json()

    return response_data["access_token"]



