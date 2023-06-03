# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from api_client import ApiClient
from http_error import HttpError
from views.view_utils import ViewUtils

from flask import Blueprint, render_template, request, redirect, url_for
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

compare_playlists_view = Blueprint("compare_playlists_view", __name__)


@compare_playlists_view.route(URL_PREFIX + "compare-playlists-by-urls", methods=["GET"])
def compare_playlists_by_urls():
    try:
        playlist_url_1 = request.args.get("playlist_url_1")
        playlist_url_2 = request.args.get("playlist_url_2")

        playlist_id_1 = ViewUtils.get_playlist_id_from_playlist_url(playlist_url_1)
        playlist_id_2 = ViewUtils.get_playlist_id_from_playlist_url(playlist_url_2)
        redirect_url = url_for(
            "compare_playlists_view.compare_playlists_by_ids",
            playlist_id_1=playlist_id_1, playlist_id_2=playlist_id_2)

        return redirect(redirect_url)
    except Exception as e:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)


@compare_playlists_view.route(URL_PREFIX + "compare-playlists", methods=["GET"])
def compare_playlists_by_ids():
    try:
        playlist_id_1 = request.args.get("playlist_id_1")
        playlist_id_2 = request.args.get("playlist_id_2")

        playlist_1 = api_client.get_playlist_by_id(playlist_id_1)
        playlist_2 = api_client.get_playlist_by_id(playlist_id_2)
        valid_attributes_for_attribute_distribution = api_client.get_valid_attributes_for_attribute_distribution()

        return render_template(
            "./compare_playlists/compare_playlists.html", playlist_1=playlist_1, playlist_2=playlist_2,
            attribute_display_names=ViewUtils.ATTRIBUTE_DISPLAY_NAMES,
            valid_attributes_for_attribute_distribution=valid_attributes_for_attribute_distribution)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
