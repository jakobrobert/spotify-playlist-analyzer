from core.utils import Utils

from flask import Blueprint, render_template
import configparser

from core.views.view_utils import ViewUtils

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

index_view = Blueprint("index_view", __name__)


@index_view.route(URL_PREFIX, methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
@ViewUtils.handle_exceptions
def index():
    return render_template("index.html")
