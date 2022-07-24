from api_client import ApiClient
from http_error import HttpError

from flask import Flask, render_template, request, redirect, url_for

import configparser
import matplotlib.pyplot as plt
from io import BytesIO
import base64

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")


@app.route(URL_PREFIX + "choose-one-playlist", methods=["GET"])
def choose_one_playlist():
    return render_template("choose_one_playlist.html")


@app.route(URL_PREFIX + "playlist-by-url", methods=["GET"])
def get_playlist_by_url():
    playlist_url = request.args.get("playlist_url")

    playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
    redirect_url = url_for("get_playlist_by_id", playlist_id=playlist_id)

    return redirect(redirect_url)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    sort_by = request.args.get("sort_by")
    order = request.args.get("order")
    filter_by = request.args.get("filter_by")
    artists_substring = request.args.get("artists_substring")
    title_substring = request.args.get("title_substring")
    min_release_year = request.args.get("min_release_year")
    max_release_year = request.args.get("max_release_year")
    min_tempo = request.args.get("min_tempo")
    max_tempo = request.args.get("max_tempo")
    expected_key = request.args.get("expected_key")
    expected_mode = request.args.get("expected_mode")
    genres_substring = request.args.get("genres_substring")
    expected_key_signature = request.args.get("expected_key_signature")

    request_params = {
        "sort_by": sort_by,
        "order": order,
        "filter_by": filter_by,
        "artists_substring": artists_substring,
        "title_substring": title_substring,
        "min_release_year": min_release_year,
        "max_release_year": max_release_year,
        "min_tempo": min_tempo,
        "max_tempo": max_tempo,
        "expected_key": expected_key,
        "expected_mode": expected_mode,
        "expected_key_signature": expected_key_signature,
        "genres_substring": genres_substring
    }

    try:
        playlist = api_client.get_playlist_by_id(playlist_id, request_params)
        valid_keys = api_client.get_valid_keys()
        valid_modes = api_client.get_valid_modes()
        valid_key_signatures = api_client.get_valid_key_signatures()
    except HttpError as error:
        return render_template("error.html", error=error)

    return render_template(
        "playlist.html", playlist=playlist, sort_by=sort_by, order=order, filter_by=filter_by,
        artists_substring=artists_substring, title_substring=title_substring,
        min_release_year=min_release_year, max_release_year=max_release_year, min_tempo=min_tempo, max_tempo=max_tempo,
        expected_key=expected_key, expected_mode=expected_mode, expected_key_signature=expected_key_signature,
        genres_substring=genres_substring,
        valid_keys=valid_keys, valid_modes=valid_modes, valid_key_signatures=valid_key_signatures
    )


@app.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
def get_attribute_distribution_of_playlist(playlist_id):
    attribute = request.args.get("attribute")

    try:
        attribute_name = __get_attribute_name(attribute)
    except Exception as e:
        error = HttpError(400, repr(e))
        return render_template("error.html", error=error)

    # TODO optimize: requesting playlist separately is overkill
    #   -> only need it in template for name & percentage_to_string()
    try:
        playlist = api_client.get_playlist_by_id(playlist_id)
        attribute_value_to_percentage = api_client.get_attribute_distribution_of_playlist(playlist_id, attribute)
    except HttpError as error:
        return render_template("error.html", error=error)

    return __render_attribute_distribution_template(playlist, attribute_name, attribute_value_to_percentage)


@app.route(URL_PREFIX + "choose-playlists-for-comparison", methods=["GET"])
def choose_playlists_for_comparison():
    return render_template("choose_playlists_for_comparison.html")


@app.route(URL_PREFIX + "compare-playlists-by-urls", methods=["GET"])
def compare_playlists_by_urls():
    playlist_url_1 = request.args.get("playlist_url_1")
    playlist_url_2 = request.args.get("playlist_url_2")
    playlist_id_1 = __get_playlist_id_from_playlist_url(playlist_url_1)
    playlist_id_2 = __get_playlist_id_from_playlist_url(playlist_url_2)
    redirect_url = url_for("compare_playlists_by_ids", playlist_id_1=playlist_id_1, playlist_id_2=playlist_id_2)

    return redirect(redirect_url)


@app.route(URL_PREFIX + "compare-playlists", methods=["GET"])
def compare_playlists_by_ids():
    playlist_id_1 = request.args.get("playlist_id_1")
    playlist_id_2 = request.args.get("playlist_id_2")

    try:
        playlist_1 = api_client.get_playlist_by_id(playlist_id_1)
        playlist_2 = api_client.get_playlist_by_id(playlist_id_2)
    except HttpError as error:
        return render_template("error.html", error=error)

    return render_template("compare_playlists.html", playlist_1=playlist_1, playlist_2=playlist_2)


@app.route(URL_PREFIX + "compare-attribute-distribution-of-playlists", methods=["GET"])
def compare_attribute_distribution_of_playlists():
    playlist_id_1 = request.args.get("playlist_id_1")
    playlist_id_2 = request.args.get("playlist_id_2")
    attribute = request.args.get("attribute")

    # TODO missing try except, see other usage
    try:
        attribute_name = __get_attribute_name(attribute)
    except Exception as e:
        error = HttpError(400, repr(e))
        return render_template("error.html", error=error)

    try:
        playlist_1 = api_client.get_playlist_by_id(playlist_id_1)
        playlist_2 = api_client.get_playlist_by_id(playlist_id_2)
        attribute_value_to_percentage_1 = api_client.get_attribute_distribution_of_playlist(playlist_id_1, attribute)
        attribute_value_to_percentage_2 = api_client.get_attribute_distribution_of_playlist(playlist_id_2, attribute)
    except HttpError as error:
        return render_template("error.html", error=error)

    return __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, attribute_name, attribute_value_to_percentage_1, attribute_value_to_percentage_2
    )


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]


def __get_attribute_name(attribute):
    if attribute == "release_year":
        return "Release Year"
    elif attribute == "tempo":
        return "Tempo (BPM)"
    elif attribute == "key":
        return "Key"
    elif attribute == "mode":
        return "Mode"
    else:
        raise ValueError(f"Invalid attribute: '{attribute}'")


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
