import configparser

from flask import Blueprint, render_template, request, redirect, url_for

from core.api_client import ApiClient
from core.playlist.spotify_track import SpotifyTrack
from core.utils import Utils
from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

playlist_view = Blueprint("playlist_view", __name__)


@playlist_view.route(URL_PREFIX + "playlist-by-url", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def get_playlist_by_url():
    playlist_url = request.args.get("playlist_url")
    playlist_id = ViewUtils.get_playlist_id_from_playlist_url(playlist_url)
    redirect_url = url_for("playlist_view.get_playlist_by_id", playlist_id=playlist_id)
    return redirect(redirect_url)


@playlist_view.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def get_playlist_by_id(playlist_id):
    pick_random_tracks_enabled = request.args.get("pick_random_tracks_enabled")
    pick_random_tracks_count = request.args.get("pick_random_tracks_count")

    api_request_params = {
        "sort_by": request.args.get("sort_by"),
        "order": request.args.get("order"),
        "pick_random_tracks_enabled": pick_random_tracks_enabled,
        "pick_random_tracks_count": pick_random_tracks_count
    }

    numerical_attributes_for_filter_option = api_client.get_numerical_attributes_for_filter_option()
    filter_params = __extract_filter_params(request.args, numerical_attributes_for_filter_option)
    api_request_params.update(filter_params)

    playlist = api_client.get_playlist_by_id(playlist_id, api_request_params)
    valid_attributes_for_attribute_distribution = api_client.get_valid_attributes_for_attribute_distribution()
    valid_attributes_for_sort_option = api_client.get_valid_attributes_for_sort_option()
    valid_key_signatures = api_client.get_valid_key_signatures()

    return render_template(
        "playlist/playlist.html", playlist=playlist,
        sort_by=api_request_params["sort_by"], order=api_request_params["order"],
        pick_random_tracks_enabled=pick_random_tracks_enabled, pick_random_tracks_count=pick_random_tracks_count,
        filter_params=filter_params,
        numerical_attributes_for_filter_option=numerical_attributes_for_filter_option,
        attribute_display_names=ViewUtils.ATTRIBUTE_DISPLAY_NAMES,
        key_strings=SpotifyTrack.KEY_STRINGS, mode_strings=SpotifyTrack.MODE_STRINGS,
        valid_attributes_for_attribute_distribution=valid_attributes_for_attribute_distribution,
        valid_attributes_for_sort_option=valid_attributes_for_sort_option,
        valid_key_signatures=valid_key_signatures
    )


@Utils.measure_execution_time(log_prefix="playlist_view.")
def __extract_filter_params(request_params, numerical_attributes_for_filter_option):
    filter_params = {
        "filter_by": request_params.get("filter_by"),
        "artists_substring": request.args.get("artists_substring"),
        "title_substring": request.args.get("title_substring"),
        "genres_substring": request.args.get("genres_substring"),
        "expected_key": Utils.get_request_arg_as_int_or_none(request.args, "expected_key"),
        "expected_mode": Utils.get_request_arg_as_int_or_none(request.args, "expected_mode"),
        "expected_key_signature": request.args.get("expected_key_signature")
    }

    filter_params.update(
        __extract_filter_params_for_numerical_attributes(request_params, numerical_attributes_for_filter_option)
    )

    return filter_params


@Utils.measure_execution_time(log_prefix="playlist_view.")
def __extract_filter_params_for_numerical_attributes(request_params, numerical_attributes_for_filter_option):
    filter_params = {}

    for attribute in numerical_attributes_for_filter_option:
        min_value_key = f"min_{attribute}"
        max_value_key = f"max_{attribute}"
        filter_params[min_value_key] = request_params.get(min_value_key)
        filter_params[max_value_key] = request_params.get(max_value_key)

    return filter_params
