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
        track_ids = request.form.getlist("track_ids[]")
        print(f"export_playlist => track_ids: {track_ids}")     # Looks fine
        if not track_ids:
            raise HttpError(status_code=400, title="export_playlist failed", message="'track_ids' is None or empty")

        exported_playlist_id = api_client.export_playlist(track_ids)
        exported_playlist_url = f"https://open.spotify.com/playlist/{exported_playlist_id}"
        return render_template("export_playlist.html", exported_playlist_url=exported_playlist_url)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
