# PyCharm shows errors for this import locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

export_playlist_view = Blueprint("export_playlist_view", __name__)


@export_playlist_view.route(URL_PREFIX + "export-playlist", methods=["GET"])
def export_playlist():
    try:
        # TODO use API endpoint to export the playlist, it returns id of the new playlist
        # TODO build playlist url based on id
        # TODO pass playlist url to template
        return render_template("export_playlist.html")
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
