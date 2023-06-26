from core.api_client import ApiClient
from core.http_error import HttpError
from core.views.view_utils import ViewUtils

from flask import Blueprint, render_template, request, redirect, url_for
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

search_tracks_view = Blueprint("search_tracks_view", __name__)


@search_tracks_view.route(URL_PREFIX + "search-tracks", methods=["GET"])
def search_tracks():
    try:
        query = request.args.get("query")
        tracks = api_client.search_tracks(query)
        return render_template(
            "search_tracks.html",
            query=query, tracks=tracks, attribute_display_names=ViewUtils.ATTRIBUTE_DISPLAY_NAMES)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
