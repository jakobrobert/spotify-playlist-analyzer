from core.http_error import HttpError
from core.utils import Utils

from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

choose_one_playlist_view = Blueprint("choose_one_playlist_view", __name__)


@choose_one_playlist_view.route(URL_PREFIX + "choose-one-playlist", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
def choose_one_playlist():
    try:
        return render_template("choose_one_playlist.html")
    except Exception:
        # TODONOW include status_code in response for all routes, as done in playlist_view.py
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
