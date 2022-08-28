# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from api_client import ApiClient
from http_error import HttpError

from flask import Blueprint, render_template, request, redirect, url_for
import configparser

playlist_view = Blueprint("playlist_view", __name__)


config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)


# TODO CLEANUP use URL_PREFIX constant. or pass url_prefix to app.register_blueprint, but did not work as expected
@playlist_view.route("/spotify-playlist-analyzer/dev/" + "playlist-by-url", methods=["GET"])
def get_playlist_by_url():
    try:
        playlist_url = request.args.get("playlist_url")

        playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
        redirect_url = url_for("playlist_view.get_playlist_by_id", playlist_id=playlist_id)

        return redirect(redirect_url)
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


# TODO CLEANUP use URL_PREFIX constant. or pass url_prefix to app.register_blueprint, but did not work as expected
@playlist_view.route("/spotify-playlist-analyzer/dev/" + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    try:
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

        playlist = api_client.get_playlist_by_id(playlist_id, request_params)
        valid_keys = api_client.get_valid_keys()
        valid_modes = api_client.get_valid_modes()
        valid_key_signatures = api_client.get_valid_key_signatures()
        valid_attributes_for_attribute_distribution = api_client.get_valid_attributes_for_attribute_distribution()

        return render_template(
            "playlist.html", playlist=playlist, sort_by=sort_by, order=order, filter_by=filter_by,
            artists_substring=artists_substring, title_substring=title_substring,
            min_release_year=min_release_year, max_release_year=max_release_year,
            min_tempo=min_tempo, max_tempo=max_tempo,
            expected_key=expected_key, expected_mode=expected_mode, expected_key_signature=expected_key_signature,
            genres_substring=genres_substring,
            valid_keys=valid_keys, valid_modes=valid_modes, valid_key_signatures=valid_key_signatures,
            valid_attributes_for_attribute_distribution=valid_attributes_for_attribute_distribution
        )
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]
