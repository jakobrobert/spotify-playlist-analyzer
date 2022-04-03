import base64

from flask import Flask, render_template, request, redirect, url_for

import configparser
import operator
import matplotlib.pyplot as plt
from io import BytesIO

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
                           playlist_id=playlist_id, sort_by="none", order="ascending")

    return redirect(redirect_url)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    sort_by = request.args.get("sort_by")
    order = request.args.get("order")

    playlist = spotify_client.get_playlist_by_id(playlist_id)
    __sort_tracks(playlist.tracks, sort_by, order)

    return render_template("playlist.html", playlist=playlist, sort_by=sort_by, order=order)


@app.route(URL_PREFIX + "playlist/<playlist_id>/year-distribution", methods=["GET"])
def get_year_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    # TODO clean up: pass data of playlist.get_year_interval_to_percentage() directly,
    #  -> need to get it here anyway to render histogram
    year_interval_to_percentage = playlist.get_year_interval_to_percentage()
    histogram_image_base64 = __get_year_distribution_histogram_image_base64(year_interval_to_percentage)

    return render_template("year_distribution.html", playlist=playlist, histogram_image_base64=histogram_image_base64)


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]


def __sort_tracks(tracks, sort_by, order):
    if sort_by == "none":
        return

    reverse = (order == "descending")
    tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)


def __get_year_distribution_histogram_image_base64(year_interval_to_percentage):
    plt.title("Year of Release Distribution")
    plt.xlabel("Year Interval")
    plt.ylabel("Percentage")

    # TODO replace by real data
    print(year_interval_to_percentage)

    """
    x_labels_years = [1980, 1990, 2000, 2010, 2020]
    y_labels_percentage = [5.0, 12.0, 42.5, 13.5, 20.6]
    # TODO clean up: hardcoding width=10 is dangerous, depends on the interval used in SpotifyPlaylist.get_year_interval_to_percentage, should pass interval to this method
    """

    x_labels_year_interval = []
    y_labels_percentage = []
    for year_interval, percentage in year_interval_to_percentage.items():
        x_labels_year_interval.append(year_interval)
        y_labels_percentage.append(percentage)

    plt.bar(x_labels_year_interval, y_labels_percentage, edgecolor="black")

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format="png")
    image_bytes = image_buffer.getvalue()
    image_base64_bytes = base64.encodebytes(image_bytes)
    image_base64_string = image_base64_bytes.decode("utf8")

    return image_base64_string
