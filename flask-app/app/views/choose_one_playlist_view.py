# PyCharm shows errors for this import locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

from flask import Blueprint, render_template

choose_one_playlist_view = Blueprint("choose_one_playlist_view", __name__)


# TODO CLEANUP use URL_PREFIX constant. or pass url_prefix to app.register_blueprint, but did not work as expected
@choose_one_playlist_view.route("/spotify-playlist-analyzer/dev/" + "choose-one-playlist", methods=["GET"])
def choose_one_playlist():
    try:
        return render_template("choose_one_playlist.html")
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)
