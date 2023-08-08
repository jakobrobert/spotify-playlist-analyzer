import configparser
from urllib.parse import urlencode

from flask import Flask, jsonify, request, redirect

from core.api_utils import ApiUtils
from core.spotify.spotify_api_client import SpotifyApiClient
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

spotify_client = SpotifyApiClient(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_TEST_REFRESH_TOKEN, SPOTIFY_TEST_USER_ID)

app = Flask(__name__)


@app.route(URL_PREFIX + "authorize", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def authorize():
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


@app.route(URL_PREFIX + "authorize/callback", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def authorize_callback():
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


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_playlist_by_id(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    playlist.tracks = ApiUtils.filter_tracks(playlist.tracks, request.args)
    ApiUtils.pick_random_tracks(playlist.tracks, request.args)
    ApiUtils.sort_tracks(playlist.tracks, request.args)

    # Need to explicitly copy the dict, else changing the dict would change the original object
    playlist_dict = dict(playlist.__dict__)

    playlist_dict["statistics"] = ApiUtils.create_playlist_statistics_dict(playlist.tracks)

    # Need to convert tracks to dict manually, playlist.__dict__ does not work recursively
    playlist_dict["tracks"] = []
    for track in playlist.tracks:
        # WARNING If you need to change track_dict, need to explicitly copy so original object will not be changed
        playlist_dict["tracks"].append(track.__dict__)

    return jsonify(playlist_dict)


@app.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_attribute_distribution_of_playlist(playlist_id):
    attribute = request.args.get("attribute")

    playlist = spotify_client.get_playlist_by_id(playlist_id)
    attribute_distribution_items = ApiUtils.get_attribute_distribution_items(attribute, playlist.tracks)

    response = jsonify(attribute_distribution_items)

    return response


@app.route(URL_PREFIX + "playlist", methods=["POST"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def create_playlist():
    request_data = request.json
    playlist_name = request_data["playlist_name"]
    track_ids = request_data["track_ids"]
    playlist_id = spotify_client.create_playlist(playlist_name, track_ids)

    return jsonify({"playlist_id": playlist_id})


@app.route(URL_PREFIX + "valid-attributes-for-attribute-distribution")
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_valid_attributes_for_attribute_distribution():
    attributes = [
        "duration_ms", "release_year", "popularity", "super_genres",
        "tempo", "key", "mode", "key_signature", "loudness",
        "danceability", "energy", "valence", "instrumentalness", "acousticness", "liveness", "speechiness"
    ]

    return jsonify(attributes)


@app.route(URL_PREFIX + "valid-attributes-for-sort-option")
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_valid_attributes_for_sort_option():
    attributes = [
        "none",
        "artists", "title", "duration_ms", "release_year", "popularity", "genres", "super_genres",
        "tempo", "key", "mode", "key_signature", "loudness",
        "danceability", "energy", "valence", "instrumentalness", "acousticness", "liveness", "speechiness"
    ]

    return jsonify(attributes)


@app.route(URL_PREFIX + "numerical-attributes-for-filter-option")
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_numerical_attributes_for_filter_option():
    return jsonify(TrackFilter.NUMERICAL_ATTRIBUTES)


@app.route(URL_PREFIX + "valid-key-signatures", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_valid_key_signatures():
    return jsonify(SpotifyTrack.KEY_SIGNATURE_STRINGS)


@app.route(URL_PREFIX + "track/<track_id>", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def get_track_by_id(track_id):
    track = spotify_client.get_track_by_id(track_id)
    # WARNING If you need to change track_dict, need to explicitly copy so original object will not be changed
    return jsonify(track.__dict__)


@app.route(URL_PREFIX + "search-tracks", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[API Endpoint] ")
@ApiUtils.handle_exceptions
def search_tracks():
    query = request.args.get("query")

    tracks = spotify_client.search_tracks(query)
    track_dicts = []

    for track in tracks:
        # Need to explicitly copy the dict, else changing the dict would change the original object
        track_dict = track.__dict__
        track_dicts.append(track_dict)

    return jsonify(track_dicts)
