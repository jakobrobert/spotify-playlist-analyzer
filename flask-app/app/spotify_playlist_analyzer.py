from api_client import ApiClient
from http_error import HttpError
from views.index_view import index_view
from views.choose_one_playlist_view import choose_one_playlist_view
from views.playlist_view import playlist_view
from views.attribute_distribution_view import attribute_distribution_view
from views.choose_playlists_for_comparison_view import choose_playlists_for_comparison_view
from views.compare_playlists_view import compare_playlists_view
from views.compare_attribute_distribution_view import compare_attribute_distribution_view

from flask import Flask, render_template, request, redirect, url_for

import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

app = Flask(__name__)
app.register_blueprint(index_view)
app.register_blueprint(choose_one_playlist_view)
app.register_blueprint(playlist_view)
app.register_blueprint(attribute_distribution_view)
app.register_blueprint(choose_playlists_for_comparison_view)
app.register_blueprint(compare_playlists_view)
app.register_blueprint(compare_attribute_distribution_view)


@app.route(URL_PREFIX + "choose-one-track", methods=["GET"])
def choose_one_track():
    try:
        return render_template("choose_one_track.html")
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


@app.route(URL_PREFIX + "track-by-url", methods=["GET"])
def get_track_by_url():
    try:
        track_url = request.args.get("track_url")

        track_id = __get_track_id_from_track_url(track_url)
        redirect_url = url_for("get_track_by_id", track_id=track_id)

        return redirect(redirect_url)
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


@app.route(URL_PREFIX + "track/<track_id>", methods=["GET"])
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
