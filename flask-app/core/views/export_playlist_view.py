from core.api_client import ApiClient
from core.http_error import HttpError
from core.utils import Utils

from flask import Blueprint, render_template, request
import configparser

from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

export_playlist_view = Blueprint("export_playlist_view", __name__)


@export_playlist_view.route(URL_PREFIX + "export-playlist", methods=["POST"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def export_playlist():
    playlist_name = request.form["playlist_name"]

    track_ids = request.form.getlist("track_ids[]")
    if not track_ids:
        raise HttpError(status_code=400, title="export_playlist failed", message="'track_ids' is None or empty")

    playlist_id = api_client.create_playlist(playlist_name, track_ids)
    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"

    return render_template("export_playlist.html", exported_playlist_url=playlist_url)
