import configparser

from flask import Blueprint, render_template

from core.utils import Utils
from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

enter_query_to_search_tracks_view = Blueprint("enter_query_to_search_tracks_view", __name__)


@enter_query_to_search_tracks_view.route(URL_PREFIX + "enter-query-to-search-tracks", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def enter_query_to_search_tracks():
    return render_template("enter_query_to_search_tracks.html")
