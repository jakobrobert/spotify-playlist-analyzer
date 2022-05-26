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
    redirect_url = url_for("get_playlist_by_id", playlist_id=playlist_id)

    return redirect(redirect_url)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    sort_by = request.args.get("sort_by") or "none"
    order = request.args.get("order") or "ascending"

    playlist = spotify_client.get_playlist_by_id(playlist_id)
    __sort_tracks(playlist.tracks, sort_by, order)

    return render_template("playlist.html", playlist=playlist, sort_by=sort_by, order=order)


@app.route(URL_PREFIX + "playlist/<playlist_id>/year-distribution", methods=["GET"])
def get_year_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)
    year_interval_to_percentage = playlist.get_year_interval_to_percentage()

    return __render_attribute_distribution_template(playlist, "Year of Release", year_interval_to_percentage)


@app.route(URL_PREFIX + "playlist/<playlist_id>/tempo-distribution", methods=["GET"])
def get_tempo_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)
    tempo_interval_to_percentage = playlist.get_tempo_interval_to_percentage()

    return __render_attribute_distribution_template(playlist, "Tempo (BPM)", tempo_interval_to_percentage)


@app.route(URL_PREFIX + "playlist/<playlist_id>/key-distribution", methods=["GET"])
def get_key_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)
    key_to_percentage = playlist.get_key_to_percentage()

    return __render_attribute_distribution_template(playlist, "Key", key_to_percentage)


@app.route(URL_PREFIX + "playlist/<playlist_id>/mode-distribution", methods=["GET"])
def get_mode_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)
    mode_to_percentage = playlist.get_mode_to_percentage()

    return __render_attribute_distribution_template(playlist, "Mode", mode_to_percentage)


@app.route(URL_PREFIX + "compare-playlists", methods=["GET"])
def compare_playlists():
    return render_template("compare_playlists.html")


@app.route(URL_PREFIX + "compare-tempo-distribution-of-playlists-by-urls", methods=["GET"])
def compare_tempo_distribution_of_playlists_by_urls():
    first_playlist_url = request.args.get("first_playlist_url")
    second_playlist_url = request.args.get("second_playlist_url")

    first_playlist_id = __get_playlist_id_from_playlist_url(first_playlist_url)
    second_playlist_id = __get_playlist_id_from_playlist_url(second_playlist_url)
    redirect_url = url_for("compare_tempo_distribution_of_playlists_by_ids",
                           first_playlist_id=first_playlist_id, second_playlist_id=second_playlist_id)

    return redirect(redirect_url)


@app.route(URL_PREFIX + "compare-tempo-distribution-of-playlists", methods=["GET"])
def compare_tempo_distribution_of_playlists_by_ids():
    first_playlist_id = request.args.get("first_playlist_id")
    second_playlist_id = request.args.get("second_playlist_id")

    first_playlist = spotify_client.get_playlist_by_id(first_playlist_id)
    second_playlist = spotify_client.get_playlist_by_id(second_playlist_id)

    tempo_interval_to_percentage_for_first_playlist = first_playlist.get_tempo_interval_to_percentage()
    tempo_interval_to_percentage_for_second_playlist = second_playlist.get_tempo_interval_to_percentage()

    return render_template("compare_attribute_distribution.html",
                           first_playlist=first_playlist, second_playlist=second_playlist,
                           attribute_name="Tempo (BPM)",
                           attribute_value_to_percentage_for_first_playlist=tempo_interval_to_percentage_for_first_playlist,
                           attribute_value_to_percentage_for_second_playlist=tempo_interval_to_percentage_for_second_playlist)


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]


def __sort_tracks(tracks, sort_by, order):
    if sort_by == "none":
        return

    reverse = (order == "descending")
    tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)


def __render_attribute_distribution_template(playlist, attribute_name, attribute_value_to_percentage):
    histogram_image_base64 = __get_histogram_image_base64(attribute_name, attribute_value_to_percentage)

    return render_template("attribute_distribution.html", playlist=playlist,
                           attribute_name=attribute_name,
                           attribute_value_to_percentage=attribute_value_to_percentage,
                           histogram_image_base64=histogram_image_base64)


def __get_histogram_image_base64(attribute_name, attribute_value_to_percentage):
    plt.title(f"{attribute_name} Distribution")
    plt.xlabel(attribute_name)
    plt.ylabel("Percentage")

    x_labels = []
    y_labels = []
    for attribute_value, percentage in attribute_value_to_percentage.items():
        x_labels.append(attribute_value)
        y_labels.append(percentage)

    plt.bar(x_labels, y_labels, edgecolor="black")
    plt.xticks(rotation=15)
    plt.tight_layout()

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format="png")
    plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
    image_bytes = image_buffer.getvalue()
    image_base64_bytes = base64.encodebytes(image_bytes)
    image_base64_string = image_base64_bytes.decode("utf8")

    return image_base64_string
