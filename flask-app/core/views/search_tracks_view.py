import configparser

from flask import Blueprint, render_template, request

from core.api_client import ApiClient
from core.utils import Utils
from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

search_tracks_view = Blueprint("search_tracks_view", __name__)


@search_tracks_view.route(URL_PREFIX + "search-tracks", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def search_tracks():
    query = request.args.get("query")
    tracks = api_client.search_tracks(query)
    return render_template(
        "search_tracks.html",
        query=query, tracks=tracks, attribute_display_names=ViewUtils.ATTRIBUTE_DISPLAY_NAMES)
