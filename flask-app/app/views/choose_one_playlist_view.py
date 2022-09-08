# PyCharm shows errors for this import locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

choose_one_playlist_view = Blueprint("choose_one_playlist_view", __name__)


@choose_one_playlist_view.route(URL_PREFIX + "choose-one-playlist", methods=["GET"])
def choose_one_playlist():
    try:
        return render_template("choose_one_playlist.html")
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
