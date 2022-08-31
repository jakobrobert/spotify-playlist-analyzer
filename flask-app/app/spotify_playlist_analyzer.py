from api_client import ApiClient
from http_error import HttpError
from views.index_view import index_view
from views.choose_one_playlist_view import choose_one_playlist_view
from views.playlist_view import playlist_view
from views.attribute_distribution_view import attribute_distribution_view
from views.choose_playlists_for_comparison_view import choose_playlists_for_comparison_view
from views.compare_playlists_view import compare_playlists_view
from views.compare_attribute_distribution_view import compare_attribute_distribution_view
from views.choose_one_track_view import choose_one_track_view
from views.track_view import track_view

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
app.register_blueprint(choose_one_track_view)
app.register_blueprint(track_view)
