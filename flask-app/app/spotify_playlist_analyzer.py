from flask import Flask, render_template, request, redirect, url_for

import configparser
import operator
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests

from spotify.spotify_client import SpotifyClient
from spotify.spotify_playlist import SpotifyPlaylist
from spotify.spotify_track import SpotifyTrack

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]

spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")


# TODO just a test endpoint, remove when REST API is implemented & integrated (#112)
@app.route(URL_PREFIX + "hello-world", methods=["GET"])
def hello_world():
    url = API_BASE_URL + "hello-world"
    response = requests.get(url)
    data = response.json()

    return data["message"]


@app.route(URL_PREFIX + "playlist-by-url", methods=["GET"])
def get_playlist_by_url():
    playlist_url = request.args.get("playlist_url")

    playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
    redirect_url = url_for("get_playlist_by_id", playlist_id=playlist_id)

    return redirect(redirect_url)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    url = f"{API_BASE_URL}playlist/{playlist_id}"

    params = {
        "sort_by": request.args.get("sort_by"),
        "order": request.args.get("order"),
        "filter_by": request.args.get("filter_by"),
        "artists_substring": request.args.get("artists_substring"),
        "title_substring": request.args.get("title_substring"),
        "min_release_year": request.args.get("min_release_year"),
        "max_release_year": request.args.get("max_release_year"),
        "min_tempo": request.args.get("min_tempo"),
        "max_tempo": request.args.get("max_tempo"),
        "expected_key": request.args.get("expected_key"),
        "expected_mode": request.args.get("expected_mode"),
        "genres_substring": request.args.get("genres_substring")
    }

    # TODO remove log
    print(f"params: {params}")

    response = requests.get(url, params=params)
    response_data = response.json()

    playlist = SpotifyPlaylist()
    playlist.id = response_data["id"]
    playlist.name = response_data["name"]

    playlist.tracks = []
    for track_data in response_data["tracks"]:
        track = SpotifyTrack()
        track.id = track_data["id"]
        track.title = track_data["title"]
        track.artist_ids = track_data["artist_ids"]
        track.artists = track_data["artists"]
        track.duration_ms = track_data["duration_ms"]
        track.release_year = track_data["release_year"]
        track.genres = track_data["genres"]
        track.tempo = track_data["tempo"]
        track.key = track_data["key"]
        track.mode = track_data["mode"]
        track.camelot = track_data["camelot"]
        track.loudness = track_data["loudness"]
        playlist.tracks.append(track)


    # TODO is duplicated code with REST API, but needs to stay here because params are needed for template
    # -> maybe can leave out the processing here, such as __get_request_param_as_int_or_none, this is probably not necessary for the template, in html everything is a string anyway

    sort_by = request.args.get("sort_by") or "none"
    order = request.args.get("order") or "ascending"

    filter_by = request.args.get("filter_by") or None
    artists_substring = request.args.get("artists_substring") or None
    title_substring = request.args.get("title_substring") or None
    min_release_year = __get_request_param_as_int_or_none("min_release_year")
    max_release_year = __get_request_param_as_int_or_none("max_release_year")
    min_tempo = __get_request_param_as_int_or_none("min_tempo")
    max_tempo = __get_request_param_as_int_or_none("max_tempo")
    expected_key = request.args.get("expected_key") or None
    expected_mode = request.args.get("expected_mode") or None
    genres_substring = request.args.get("genres_substring") or None

    return render_template(
        "playlist.html", playlist=playlist, sort_by=sort_by, order=order, filter_by=filter_by,
        artists_substring=artists_substring,
        min_release_year=min_release_year, max_release_year=max_release_year, min_tempo=min_tempo, max_tempo=max_tempo,
        expected_key=expected_key, expected_mode=expected_mode,
        genres_substring=genres_substring, title_substring=title_substring
    )


@app.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
def get_attribute_distribution_of_playlist(playlist_id):
    attribute = request.args.get("attribute")
    
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    if attribute == "release_year":
        attribute_name = "Release Year"
        attribute_value_to_percentage = playlist.get_release_year_interval_to_percentage()
    elif attribute == "tempo":
        attribute_name = "Tempo (BPM)"
        attribute_value_to_percentage = playlist.get_tempo_interval_to_percentage()
    elif attribute == "key":
        attribute_name = "Key"
        attribute_value_to_percentage = playlist.get_key_to_percentage()
    elif attribute == "mode":
        attribute_name = "Mode"
        attribute_value_to_percentage = playlist.get_mode_to_percentage()
    else:
        raise ValueError(f"Unknown attribute: '{attribute}'")

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
    playlist_1 = spotify_client.get_playlist_by_id(playlist_id_1)
    playlist_2 = spotify_client.get_playlist_by_id(playlist_id_2)

    return render_template("compare_playlists.html", playlist_1=playlist_1, playlist_2=playlist_2)


@app.route(URL_PREFIX + "compare-attribute-distribution-of-playlists", methods=["GET"])
def compare_attribute_distribution_of_playlists():
    playlist_id_1 = request.args.get("playlist_id_1")
    playlist_id_2 = request.args.get("playlist_id_2")
    attribute = request.args.get("attribute")

    playlist_1 = spotify_client.get_playlist_by_id(playlist_id_1)
    playlist_2 = spotify_client.get_playlist_by_id(playlist_id_2)

    if attribute == "release_year":
        attribute_name = "Release Year"
        attribute_value_to_percentage_1 = playlist_1.get_release_year_interval_to_percentage()
        attribute_value_to_percentage_2 = playlist_2.get_release_year_interval_to_percentage()
    elif attribute == "tempo":
        attribute_name = "Tempo (BPM)"
        attribute_value_to_percentage_1 = playlist_1.get_tempo_interval_to_percentage()
        attribute_value_to_percentage_2 = playlist_2.get_tempo_interval_to_percentage()
    elif attribute == "key":
        attribute_name = "Key"
        attribute_value_to_percentage_1 = playlist_1.get_key_to_percentage()
        attribute_value_to_percentage_2 = playlist_2.get_key_to_percentage()
    elif attribute == "mode":
        attribute_name = "Mode"
        attribute_value_to_percentage_1 = playlist_1.get_mode_to_percentage()
        attribute_value_to_percentage_2 = playlist_2.get_mode_to_percentage()
    else:
        raise ValueError(f"Unknown attribute: '{attribute}'")

    return __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, attribute_name, attribute_value_to_percentage_1, attribute_value_to_percentage_2
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


def __get_request_param_as_int_or_none(name):
    value_string = request.args.get(name) or None

    if value_string:
        return int(value_string)

    return None


def __filter_tracks(tracks, filter_by, min_tempo, max_tempo, min_release_year, max_release_year,
                    artists_substring, genres_substring, expected_key, expected_mode, title_substring):
    if filter_by is None:
        return tracks

    if filter_by == "artists":
        if artists_substring is None:
            raise ValueError("artists_substring must be defined to filter by artists!")

        return list(filter(lambda track: any(artists_substring in artist for artist in track.artists), tracks))

    if filter_by == "title":
        if title_substring is None:
            raise ValueError("title_substring must be defined to filter by title!")

        return list(filter(lambda track: title_substring in track.title, tracks))

    if filter_by == "release_year":
        if min_release_year is None:
            raise ValueError("min_release_year must be defined to filter by release_year!")

        if max_release_year is None:
            raise ValueError("max_release_year must be defined to filter by release_year!")

        return list(filter(lambda track: min_release_year <= track.release_year <= max_release_year, tracks))

    if filter_by == "tempo":
        if min_tempo is None:
            raise ValueError("min_tempo must be defined to filter by tempo!")

        if max_tempo is None:
            raise ValueError("max_tempo must be defined to filter by tempo!")

        return list(filter(lambda track: min_tempo <= track.tempo <= max_tempo, tracks))

    if filter_by == "key":
        if expected_key is None:
            raise ValueError("expected_key must be defined to filter by key!")

        return list(filter(lambda track: track.get_key_string() == expected_key, tracks))
    
    if filter_by == "mode":
        if expected_mode is None:
            raise ValueError("expected_mode must be defined to filter by mode!")

        return list(filter(lambda track: track.get_mode_string() == expected_mode, tracks))

    if filter_by == "genres":
        if genres_substring is None:
            raise ValueError("genres_substring must be defined to filter by genres!")

        return list(filter(lambda track: any(genres_substring in genre for genre in track.genres), tracks))

    raise ValueError(f"This attribute is not supported to filter by: {filter_by}")


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
