from core.utils import Utils

from flask import Blueprint, render_template
import configparser

from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

choose_playlists_for_comparison_view = Blueprint("choose_playlists_for_comparison_view", __name__)


@choose_playlists_for_comparison_view.route(URL_PREFIX + "choose-playlists-for-comparison", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def choose_playlists_for_comparison():
    return render_template("choose_playlists_for_comparison.html")
