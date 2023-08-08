import configparser

from flask import Blueprint, render_template

from core.utils import Utils
from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

choose_one_playlist_view = Blueprint("choose_one_playlist_view", __name__)


@choose_one_playlist_view.route(URL_PREFIX + "choose-one-playlist", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def choose_one_playlist():
    return render_template("choose_one_playlist.html")
