# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from api_client import ApiClient
from http_error import HttpError

from flask import Blueprint, render_template, request
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

export_playlist_view = Blueprint("export_playlist_view", __name__)


@export_playlist_view.route(URL_PREFIX + "export-playlist", methods=["POST"])
def export_playlist():
    try:
        # TODO read from form, once implemented in template
        playlist_name = "BLA BLA"
        if not playlist_name:
            raise HttpError(status_code=400, title="export_playlist failed", message="'playlist_name' is None or empty")

        track_ids = request.form.getlist("track_ids[]")
        if not track_ids:
            raise HttpError(status_code=400, title="export_playlist failed", message="'track_ids' is None or empty")

        playlist_id = api_client.create_playlist(playlist_name, track_ids)
        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
        return render_template("export_playlist.html", exported_playlist_url=playlist_url)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
