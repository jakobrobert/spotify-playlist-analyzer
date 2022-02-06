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

    playlist_id_start_index = playlist_url.find("playlist/") + len("playlist/")
    playlist_id_end_index = playlist_url.find("?")
    playlist_id = playlist_url[playlist_id_start_index:playlist_id_end_index]

    # TODO this is just a test token, use proper Authentication flow
    access_token = "BQBPTOQbOcNgbylEde97_eMLX4AilcQxnEMP0WuaDvmex_5CeGUW3IwCECcQ4xCtze3xsgdh9UPyEMzu5u9XxXkweHTTm1wjBTd97IGQBJa8zIBdEpbU3N7hVU2ZQ2Z8Mha0JSCu40YRUrveFb-ScFXn17KeWyjbgnI "
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    response = requests.get(url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    response_data = response.json()
    tracks = response_data["tracks"]["items"]

    songs = []

    # TODO this contains only 100 songs, even though playlist has more songs. need to set limit param or send several requests?
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
