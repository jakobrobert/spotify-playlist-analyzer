# PyCharm shows errors for this import locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

enter_query_to_search_tracks_view = Blueprint("enter_query_to_search_tracks_view", __name__)


@enter_query_to_search_tracks_view.route(URL_PREFIX + "enter-query-to-search-tracks", methods=["GET"])
def enter_query_to_search_tracks():
    try:
        return render_template("enter_query_to_search_tracks.html")
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
