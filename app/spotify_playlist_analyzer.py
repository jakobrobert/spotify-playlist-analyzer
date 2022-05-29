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


@app.route(URL_PREFIX + "choose-playlists-for-comparison", methods=["GET"])
def choose_playlists_for_comparison():
    return render_template("choose_playlists_for_comparison.html")


@app.route(URL_PREFIX + "compare-playlists", methods=["GET"])
def compare_playlists():
    # TODO add in between page so it can be shared / bookmarked
    playlist_url_1 = request.args.get("playlist_url_1")
    print(f"playlist_url_1: {playlist_url_1}")
    playlist_url_2 = request.args.get("playlist_url_2")
    print(f"playlist_url_2: {playlist_url_2}")
    playlist_id_1 = __get_playlist_id_from_playlist_url(playlist_url_1)
    print(f"playlist_id_1: {playlist_id_1}")
    playlist_id_2 = __get_playlist_id_from_playlist_url(playlist_url_2)
    print(f"playlist_id_2: {playlist_id_2}")

    playlist_1 = spotify_client.get_playlist_by_id(playlist_id_1)
    playlist_2 = spotify_client.get_playlist_by_id(playlist_id_2)

    return render_template("compare_playlists.html", playlist_1=playlist_1, playlist_2=playlist_2)


@app.route(URL_PREFIX + "compare-year-distribution-of-playlists-by-urls", methods=["GET"])
def compare_year_distribution_of_playlists_by_urls():
    return __redirect_compare_attribute_distribution_from_urls_to_ids("compare_year_distribution_of_playlists_by_ids")


@app.route(URL_PREFIX + "compare-year-distribution-of-playlists", methods=["GET"])
def compare_year_distribution_of_playlists_by_ids():
    playlist_1, playlist_2 = __get_playlists_to_compare_attribute_distribution()
    year_interval_to_percentage_1 = playlist_1.get_year_interval_to_percentage()
    year_interval_to_percentage_2 = playlist_2.get_year_interval_to_percentage()

    return __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, "Year of Release", year_interval_to_percentage_1, year_interval_to_percentage_2
    )


# TODO clean up: move function down to other private ones
def __redirect_compare_attribute_distribution_from_urls_to_ids(endpoint):
    playlist_url_1 = request.args.get("playlist_url_1")
    playlist_url_2 = request.args.get("playlist_url_2")
    playlist_id_1 = __get_playlist_id_from_playlist_url(playlist_url_1)
    playlist_id_2 = __get_playlist_id_from_playlist_url(playlist_url_2)
    redirect_url = url_for(endpoint, playlist_id_1=playlist_id_1, playlist_id_2=playlist_id_2)

    return redirect(redirect_url)


@app.route(URL_PREFIX + "compare-tempo-distribution-of-playlists-by-urls", methods=["GET"])
def compare_tempo_distribution_of_playlists_by_urls():
    return __redirect_compare_attribute_distribution_from_urls_to_ids("compare_tempo_distribution_of_playlists_by_ids")


@app.route(URL_PREFIX + "compare-tempo-distribution-of-playlists", methods=["GET"])
def compare_tempo_distribution_of_playlists_by_ids():
    playlist_1, playlist_2 = __get_playlists_to_compare_attribute_distribution()
    tempo_interval_to_percentage_1 = playlist_1.get_tempo_interval_to_percentage()
    tempo_interval_to_percentage_2 = playlist_2.get_tempo_interval_to_percentage()

    return __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, "Tempo (BPM)", tempo_interval_to_percentage_1, tempo_interval_to_percentage_2
    )


@app.route(URL_PREFIX + "compare-key-distribution-of-playlists-by-urls", methods=["GET"])
def compare_key_distribution_of_playlists_by_urls():
    return __redirect_compare_attribute_distribution_from_urls_to_ids("compare_key_distribution_of_playlists_by_ids")


@app.route(URL_PREFIX + "compare-key-distribution-of-playlists", methods=["GET"])
def compare_key_distribution_of_playlists_by_ids():
    playlist_1, playlist_2 = __get_playlists_to_compare_attribute_distribution()
    key_to_percentage_1 = playlist_1.get_key_to_percentage()
    key_to_percentage_2 = playlist_2.get_key_to_percentage()

    return __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, "Key", key_to_percentage_1, key_to_percentage_2
    )


@app.route(URL_PREFIX + "compare-mode-distribution-of-playlists-by-urls", methods=["GET"])
def compare_mode_distribution_of_playlists_by_urls():
    return __redirect_compare_attribute_distribution_from_urls_to_ids("compare_mode_distribution_of_playlists_by_ids")


@app.route(URL_PREFIX + "compare-mode-distribution-of-playlists", methods=["GET"])
def compare_mode_distribution_of_playlists_by_ids():
    playlist_1, playlist_2 = __get_playlists_to_compare_attribute_distribution()
    mode_to_percentage_1 = playlist_1.get_mode_to_percentage()
    mode_to_percentage_2 = playlist_2.get_mode_to_percentage()

    return __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, "mode", mode_to_percentage_1, mode_to_percentage_2
    )


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

    return __get_image_base64_from_plot()


def __get_image_base64_from_plot():
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format="png")
    plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
    image_bytes = image_buffer.getvalue()
    image_base64_bytes = base64.encodebytes(image_bytes)
    image_base64_string = image_base64_bytes.decode("utf8")

    return image_base64_string


def __get_playlists_to_compare_attribute_distribution():
    playlist_id_1 = request.args.get("playlist_id_1")
    playlist_id_2 = request.args.get("playlist_id_2")
    playlist_1 = spotify_client.get_playlist_by_id(playlist_id_1)
    playlist_2 = spotify_client.get_playlist_by_id(playlist_id_2)

    return playlist_1, playlist_2


def __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, attribute_name, attribute_value_to_percentage_1, attribute_value_to_percentage_2):
    chart_image_base64 = __get_attribute_comparison_chart_image_base64(
        attribute_name, playlist_1.name, playlist_2.name,
        attribute_value_to_percentage_1, attribute_value_to_percentage_2
    )

    return render_template("compare_attribute_distribution.html",
                           playlist_1=playlist_1, playlist_2=playlist_2, attribute_name=attribute_name,
                           attribute_value_to_percentage_1=attribute_value_to_percentage_1,
                           attribute_value_to_percentage_2=attribute_value_to_percentage_2,
                           chart_image_base64=chart_image_base64)


def __get_attribute_comparison_chart_image_base64(attribute_name, playlist_name_1, playlist_name_2,
                                                  attribute_value_to_percentage_1, attribute_value_to_percentage_2):
    plt.title(f"Compare {attribute_name} Distribution")
    plt.xlabel(attribute_name)
    plt.ylabel("Percentage")

    x_labels = []
    y_labels_1 = []
    y_labels_2 = []
    for attribute_value in attribute_value_to_percentage_1.keys():
        x_labels.append(attribute_value)
        y_labels_1.append(attribute_value_to_percentage_1[attribute_value])
        y_labels_2.append(attribute_value_to_percentage_2[attribute_value])

    plt.bar(x_labels, y_labels_1, fill=False, linewidth=2, edgecolor="red", label=playlist_name_1)
    plt.bar(x_labels, y_labels_2, fill=False, linewidth=2, edgecolor="blue", label=playlist_name_2)
    plt.xticks(rotation=15)
    plt.legend()
    plt.tight_layout()

    return __get_image_base64_from_plot()
