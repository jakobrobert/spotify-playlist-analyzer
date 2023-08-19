import configparser

from flask import Blueprint, render_template, request, redirect, url_for

from core.api_client import ApiClient
from core.utils import Utils
from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

track_view = Blueprint("track_view", __name__)


@track_view.route(URL_PREFIX + "track-by-url", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def get_track_by_url():
    track_url = request.args.get("track_url")
    track_id = ViewUtils.get_track_id_from_track_url(track_url)
    redirect_url = url_for("track_view.get_track_by_id", track_id=track_id)
    return redirect(redirect_url)


@track_view.route(URL_PREFIX + "track/<track_id>", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
#@ViewUtils.handle_exceptions # TODONOW REVERT
def get_track_by_id(track_id):
    track = api_client.get_track_by_id(track_id)
    return render_template("track.html", track=track, attribute_display_names=ViewUtils.ATTRIBUTE_DISPLAY_NAMES)
