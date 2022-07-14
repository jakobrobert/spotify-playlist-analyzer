import configparser
import operator

from flask import Flask, jsonify, request

from spotify.spotify_client import SpotifyClient
from spotify.spotify_track import SpotifyTrack

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]

spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

app = Flask(__name__)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    sort_by = request.args.get("sort_by") or "none"
    order = request.args.get("order") or "ascending"
    __sort_tracks(playlist.tracks, sort_by, order)

    filter_by = request.args.get("filter_by") or None
    artists_substring = request.args.get("artists_substring") or None
    title_substring = request.args.get("title_substring") or None
    min_release_year = __get_request_param_as_int_or_none("min_release_year")
    max_release_year = __get_request_param_as_int_or_none("max_release_year")
    min_tempo = __get_request_param_as_int_or_none("min_tempo")
    max_tempo = __get_request_param_as_int_or_none("max_tempo")
    expected_key = request.args.get("expected_key") or None
    expected_mode = request.args.get("expected_mode") or None
    expected_key_signature = request.args.get("expected_key_signature") or None
    genres_substring = request.args.get("genres_substring") or None

    playlist.tracks = __filter_tracks(
        playlist.tracks, filter_by,
        artists_substring, title_substring, min_release_year, max_release_year, min_tempo, max_tempo,
        expected_key, expected_mode, expected_key_signature, genres_substring
    )

    # Need to explicitly copy the dict, else changing the dict would change the original object
    playlist_dict = dict(playlist.__dict__)

    # Add calculated values
    playlist_dict["total_duration_ms"] = playlist.get_total_duration_ms()
    playlist_dict["average_duration_ms"] = playlist.get_average_duration_ms()
    playlist_dict["average_release_year"] = playlist.get_average_release_year()
    playlist_dict["average_tempo"] = playlist.get_average_tempo()

    # Need to convert tracks to dict manually, playlist.__dict__ does not work recursively
    playlist_dict["tracks"] = []
    for track in playlist.tracks:
        track_dict = dict(track.__dict__)
        # Overwrite values for key & mode so API returns them as strings instead of numbers
        track_dict["key"] = track.get_key_string()
        track_dict["mode"] = track.get_mode_string()
        playlist_dict["tracks"].append(track_dict)

    return jsonify(playlist_dict)


@app.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
def get_attribute_distribution_of_playlist(playlist_id):
    attribute = request.args.get("attribute")

    playlist = spotify_client.get_playlist_by_id(playlist_id)

    if attribute == "release_year":
        attribute_value_to_percentage = playlist.get_release_year_interval_to_percentage()
    elif attribute == "tempo":
        attribute_value_to_percentage = playlist.get_tempo_interval_to_percentage()
    elif attribute == "key":
        attribute_value_to_percentage = playlist.get_key_to_percentage()
    elif attribute == "mode":
        attribute_value_to_percentage = playlist.get_mode_to_percentage()
    else:
        raise ValueError(f"Unknown attribute: '{attribute}'")

    return jsonify(attribute_value_to_percentage)


@app.route(URL_PREFIX + "valid-keys", methods=["GET"])
def get_valid_keys():
    return jsonify(SpotifyTrack.KEY_STRINGS)


@app.route(URL_PREFIX + "valid-modes", methods=["GET"])
def get_valid_modes():
    return jsonify(SpotifyTrack.MODE_STRINGS)


def __sort_tracks(tracks, sort_by, order):
    if sort_by == "none":
        return

    reverse = (order == "descending")
    tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)


def __filter_tracks(
        tracks, filter_by,
        artists_substring, title_substring, min_release_year, max_release_year, min_tempo, max_tempo,
        expected_key, expected_mode, expected_key_signature, genres_substring
):
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

    if filter_by == "key_signature":
        if expected_key_signature is None:
            raise ValueError("expected_key_signature must be defined to filter by key_signature!")

        return list(filter(lambda track: track.key_signature == expected_key_signature, tracks))

    if filter_by == "genres":
        if genres_substring is None:
            raise ValueError("genres_substring must be defined to filter by genres!")

        return list(filter(lambda track: any(genres_substring in genre for genre in track.genres), tracks))

    raise ValueError(f"This attribute is not supported to filter by: {filter_by}")


def __get_request_param_as_int_or_none(name):
    value_string = request.args.get(name) or None

    if value_string:
        return int(value_string)

    return None
