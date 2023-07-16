import configparser
import operator
import random
from urllib.parse import urlencode

from flask import Flask, jsonify, request, redirect

from core.filter_params import FilterParams
from core.http_error import HttpError
from core.playlist_statistics.playlist_statistics import PlaylistStatistics
from core.spotify.spotify_client import SpotifyClient
from core.spotify.spotify_track import SpotifyTrack
from core.track_filter import TrackFilter
from core.utils import Utils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
SPOTIFY_CLIENT_ID = config["SPOTIFY"]["CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["SPOTIFY"]["CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = config["SPOTIFY"]["REDIRECT_URI"]
SPOTIFY_TEST_REFRESH_TOKEN = config["SPOTIFY"]["TEST_REFRESH_TOKEN"]
SPOTIFY_TEST_USER_ID = config["SPOTIFY"]["TEST_USER_ID"]

spotify_client = SpotifyClient(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_TEST_REFRESH_TOKEN, SPOTIFY_TEST_USER_ID)

app = Flask(__name__)


@app.route(URL_PREFIX + "authorize", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def authorize():
    try:
        authorization_base_url = "https://accounts.spotify.com/authorize"
        # Cannot use url_for to get redirect uri because url_for just returns part of the url, but need the full
        # Therefore hardcoded it in ini file.
        # TODOLATER #171 can use url_for, need to set _external=True
        params = {
            "client_id": SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "scope": "playlist-modify-public"
        }
        params_encoded = urlencode(params)
        authorization_url = f"{authorization_base_url}?{params_encoded}"

        return redirect(authorization_url)
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "authorize/callback", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def authorize_callback():
    try:
        if "code" not in request.args:
            raise ValueError("Failed to get authorization code because request arg 'code' is missing")

        authorization_code = request.args.get("code")
        print(f"authorize_callback => authorization_code: {authorization_code}")

        response_data = spotify_client.get_access_and_refresh_token(authorization_code)

        access_token = response_data["access_token"]
        print(f"authorize_callback => access_token: {access_token}")
        refresh_token = response_data["refresh_token"]
        print(f"authorize_callback => refresh_token: {refresh_token}")

        # Write access token to file.
        # TODOLATER #171 This is a workaround, because getting access token by refresh token fails.
        #   -> Need to manually authorize so users can create playlist for the test account
        #   -> But with this workaround, can do it comfortably in browser, on phone.
        #   -> No need to manually update the access code in ini
        test_access_token_config = configparser.ConfigParser()
        test_access_token_config.add_section("SPOTIFY")
        test_access_token_config.set("SPOTIFY", "TEST_ACCESS_TOKEN", access_token)

        file_name = "./test_access_token.ini"
        with open(file_name, "w") as config_file:
            test_access_token_config.write(config_file)

        return f"Authorization was successful. Written access token to file '{file_name}'"
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_playlist_by_id(playlist_id):
    try:
        playlist = spotify_client.get_playlist_by_id(playlist_id)

        playlist.tracks = __filter_tracks(playlist.tracks, request.args)
        __pick_random_tracks(playlist.tracks, request.args)
        __sort_tracks(playlist.tracks, request.args)

        statistics = PlaylistStatistics(playlist.tracks)

        # Need to explicitly copy the dict, else changing the dict would change the original object
        playlist_dict = dict(playlist.__dict__)

        # Add calculated values
        playlist_dict["total_duration_ms"] = statistics.get_total_duration_ms()
        playlist_dict["average_duration_ms"] = statistics.get_average_duration_ms()
        playlist_dict["average_release_year"] = statistics.get_average_release_year()
        playlist_dict["average_popularity"] = statistics.get_average_popularity()
        playlist_dict["average_tempo"] = statistics.get_average_tempo()

        # Need to convert tracks to dict manually, playlist.__dict__ does not work recursively
        playlist_dict["tracks"] = []
        for track in playlist.tracks:
            track_dict = __convert_track_to_dict(track)
            playlist_dict["tracks"].append(track_dict)

        return jsonify(playlist_dict)
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def __filter_tracks(tracks, request_args):
    filter_params = FilterParams.extract_filter_params_from_request_params(request_args)
    track_filter = TrackFilter(tracks, filter_params)
    return track_filter.filter_tracks()


@app.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_attribute_distribution_of_playlist(playlist_id):
    try:
        attribute = request.args.get("attribute")

        playlist = spotify_client.get_playlist_by_id(playlist_id)
        attribute_distribution_items = __get_attribute_distribution_items(attribute, playlist.tracks)

        response = jsonify(attribute_distribution_items)

        return response
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "playlist", methods=["POST"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def create_playlist():
    try:
        request_data = request.json
        playlist_name = request_data["playlist_name"]
        track_ids = request_data["track_ids"]
        playlist_id = spotify_client.create_playlist(playlist_name, track_ids)

        return jsonify({"playlist_id": playlist_id})
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "valid-attributes-for-attribute-distribution")
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_valid_attributes_for_attribute_distribution():
    try:
        attributes = [
            "duration_ms", "release_year", "popularity",

            # Audio Features
            "tempo", "key", "mode", "key_signature", "loudness",
            "danceability", "energy", "valence", "instrumentalness", "acousticness", "liveness", "speechiness"
        ]

        return jsonify(attributes)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "valid-attributes-for-sort-option")
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_valid_attributes_for_sort_option():
    try:
        attributes = [
            "none",
            "artists", "title", "duration_ms", "release_year", "popularity", "genres",

            # Audio Features
            "tempo", "key", "mode", "key_signature", "loudness",
            "danceability", "energy", "valence", "instrumentalness", "acousticness", "liveness", "speechiness"
            ]

        return jsonify(attributes)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "numerical-attributes-for-filter-option")
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_numerical_attributes_for_filter_option():
    try:
        return jsonify(TrackFilter.NUMERICAL_ATTRIBUTES)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "valid-keys", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_valid_keys():
    try:
        return jsonify(SpotifyTrack.KEY_STRINGS)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "valid-modes", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_valid_modes():
    try:
        return jsonify(SpotifyTrack.MODE_STRINGS)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "valid-key-signatures", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_valid_key_signatures():
    try:
        return jsonify(SpotifyTrack.KEY_SIGNATURE_STRINGS)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "track/<track_id>", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def get_track_by_id(track_id):
    try:
        track = spotify_client.get_track_by_id(track_id)
        track_dict = __convert_track_to_dict(track)

        return jsonify(track_dict)
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@app.route(URL_PREFIX + "search-tracks", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
def search_tracks():
    try:
        query = request.args.get("query")

        tracks = spotify_client.search_tracks(query)
        track_dicts = []

        for track in tracks:
            track_dict = __convert_track_to_dict(track)
            track_dicts.append(track_dict)

        return jsonify(track_dicts)
    except HttpError as error:
        return __create_error_response(error)
    except Exception:
        error = HttpError.from_last_exception()
        return __create_error_response(error)


@Utils.measure_execution_time(log_prefix="[API Helper] ")
def __pick_random_tracks(tracks, request_args):
    pick_random_tracks_enabled = request_args.get("pick_random_tracks_enabled") == "on"
    if not pick_random_tracks_enabled:
        return

    pick_random_tracks_count = __get_request_param_as_int_or_none(request_args, "pick_random_tracks_count")
    if pick_random_tracks_count is None:
        raise HttpError(400, "API Error", "Missing request arg 'pick_random_tracks_count'")

    if pick_random_tracks_count < 0:
        raise HttpError(
            400, "API Error",
            "Invalid value for request arg 'pick_random_tracks_count' -> must be > 0"
        )

    if pick_random_tracks_count >= len(tracks):
        raise HttpError(
            400, "API Error",
            "Invalid value for request arg 'pick_random_tracks_count' -> must be < number of tracks after filtering"
        )

    random.shuffle(tracks)
    del tracks[pick_random_tracks_count:]


@Utils.measure_execution_time(log_prefix="[API Helper] ")
def __sort_tracks(tracks, request_args):
    sort_by = request_args.get("sort_by") or None
    order = request_args.get("order") or "ascending"

    if sort_by is None:
        return

    reverse = (order == "descending")
    tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)

def __create_error_response(error):
    # Need to convert traceback_items manually, __dict__ is not supported
    traceback_items_converted = []

    for traceback_item in error.traceback_items:
        traceback_item_converted = []

        for traceback_item_attribute in traceback_item:
            traceback_item_converted.append(str(traceback_item_attribute))

        traceback_items_converted.append(traceback_item_converted)

    response_data = {
        "error": {
            "status_code": error.status_code,
            "title": error.title,
            "message": error.message,
            "traceback_items": traceback_items_converted
        }
    }
    response = jsonify(response_data)

    return response, error.status_code


def __convert_track_to_dict(track):
    # Need to explicitly copy the dict, else changing the dict would change the original object
    track_dict = dict(track.__dict__)

    # Overwrite values for key & mode so API returns them as strings instead of numbers
    track_dict["key"] = track.get_key_string()
    track_dict["mode"] = track.get_mode_string()

    return track_dict


def __get_attribute_distribution_items(attribute, tracks):
    statistics = PlaylistStatistics(tracks)

    if attribute == "duration_ms":
        return statistics.get_duration_distribution_items()
    if attribute == "release_year":
        return statistics.get_release_year_distribution_items()
    if attribute == "popularity":
        return statistics.get_popularity_distribution_items()

    # Audio Features
    if attribute == "tempo":
        return statistics.get_tempo_distribution_items()
    if attribute == "key":
        return statistics.get_key_distribution_items()
    if attribute == "mode":
        return statistics.get_mode_distribution_items()
    if attribute == "key_signature":
        return statistics.get_key_signature_distribution_items()
    if attribute == "loudness":
        return statistics.get_loudness_distribution_items()
    if attribute == "danceability":
        return statistics.get_danceability_distribution_items()
    if attribute == "energy":
        return statistics.get_energy_distribution_items()
    if attribute == "valence":
        return statistics.get_valence_distribution_items()
    if attribute == "instrumentalness":
        return statistics.get_instrumentalness_distribution_items()
    if attribute == "acousticness":
        return statistics.get_acousticness_distribution_items()
    if attribute == "liveness":
        return statistics.get_liveness_distribution_items()
    if attribute == "speechiness":
        return statistics.get_speechiness_distribution_items()

    raise HttpError(400, "API Error", f"Invalid attribute: '{attribute}'")


# TODONOW extract helper method to Utils
def __get_request_param_as_int_or_none(request_params, name):
    value_string = request_params.get(name)

    if value_string:
        return int(value_string)

    return None