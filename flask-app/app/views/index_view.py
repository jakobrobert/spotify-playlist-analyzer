# PyCharm shows errors for this import locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

index_view = Blueprint("index_view", __name__)


@index_view.route(URL_PREFIX, methods=["GET"])
def index():
    try:
        return render_template("index.html")
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)
