from core.utils import Utils

from flask import Blueprint, render_template
import configparser

from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

choose_one_track_view = Blueprint("choose_one_track_view", __name__)


@choose_one_track_view.route(URL_PREFIX + "choose-one-track", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def choose_one_track():
    return render_template("choose_one_track.html")
