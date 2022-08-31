# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from api_client import ApiClient
from http_error import HttpError

from flask import Blueprint, render_template, request, redirect, url_for
import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

track_view = Blueprint("track_view", __name__)


@track_view.route(URL_PREFIX + "track-by-url", methods=["GET"])
def get_track_by_url():
    try:
        track_url = request.args.get("track_url")

        track_id = __get_track_id_from_track_url(track_url)
        redirect_url = url_for("track_view.get_track_by_id", track_id=track_id)

        return redirect(redirect_url)
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


@track_view.route(URL_PREFIX + "track/<track_id>", methods=["GET"])
def get_track_by_id(track_id):
    try:
        track = api_client.get_track_by_id(track_id)
        return render_template("track.html", track=track)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


def __get_track_id_from_track_url(track_url):
    start_index = track_url.find("track/") + len("track/")
    end_index = track_url.find("?")

    return track_url[start_index:end_index]
