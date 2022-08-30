# PyCharm shows errors for this import locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

choose_playlists_for_comparison_view = Blueprint("choose_playlists_for_comparison_view", __name__)


@choose_playlists_for_comparison_view.route(URL_PREFIX + "choose-playlists-for-comparison", methods=["GET"])
def choose_playlists_for_comparison():
    try:
        return render_template("choose_playlists_for_comparison.html")
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)
