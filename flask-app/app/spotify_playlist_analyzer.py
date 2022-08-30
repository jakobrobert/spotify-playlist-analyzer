from api_client import ApiClient
from http_error import HttpError
from views.index_view import index_view
from views.choose_one_playlist_view import choose_one_playlist_view
from views.playlist_view import playlist_view
from views.attribute_distribution_view import attribute_distribution_view
from views.choose_playlists_for_comparison_view import choose_playlists_for_comparison_view
from views.compare_playlists_view import compare_playlists_view

from flask import Flask, render_template, request, redirect, url_for

import configparser
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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


@app.route(URL_PREFIX + "compare-attribute-distribution-of-playlists", methods=["GET"])
def compare_attribute_distribution_of_playlists():
    try:
        playlist_id_1 = request.args.get("playlist_id_1")
        playlist_id_2 = request.args.get("playlist_id_2")
        attribute = request.args.get("attribute")

        attribute_name = __get_attribute_display_name(attribute)

        playlist_1 = api_client.get_playlist_by_id(playlist_id_1)
        playlist_2 = api_client.get_playlist_by_id(playlist_id_2)
        attribute_value_to_percentage_1 = api_client.get_attribute_distribution_of_playlist(playlist_id_1, attribute)
        attribute_value_to_percentage_2 = api_client.get_attribute_distribution_of_playlist(playlist_id_2, attribute)

        return __render_compare_attribute_distribution_template(
            playlist_1, playlist_2, attribute_name, attribute_value_to_percentage_1, attribute_value_to_percentage_2)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception as e:
        error = HttpError(502, repr(e))
        return render_template("error.html", error=error)


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


# TODO CLEANUP these helper methods are duplicated, see attribute_distribution_view.py, extract into Utils class
def __get_attribute_display_name(attribute_name):
    attributes = api_client.get_valid_attributes_for_attribute_distribution()

    for attribute in attributes:
        if attribute["name"] == attribute_name:
            return attribute["display_name"]

    raise ValueError(f"Invalid attribute: '{attribute_name}'")


# TODO CLEANUP these helper methods are duplicated, extract into Utils class
def __get_image_base64_from_plot():
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format="png")
    plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
    image_bytes = image_buffer.getvalue()
    image_base64_bytes = base64.encodebytes(image_bytes)
    image_base64_string = image_base64_bytes.decode("utf8")

    return image_base64_string


def __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, attribute_name, attribute_value_to_percentage_1, attribute_value_to_percentage_2):
    chart_image_base64 = __get_attribute_comparison_chart_image_base64(
        attribute_name, playlist_1.name, playlist_2.name,
        attribute_value_to_percentage_1, attribute_value_to_percentage_2
    )

    return render_template("compare_attribute_distribution.html",
                           playlist_1=playlist_1, playlist_2=playlist_2, attribute_name=attribute_name,
                           attribute_value_to_percentage_1=attribute_value_to_percentage_1,
                           attribute_value_to_percentage_2=attribute_value_to_percentage_2,
                           chart_image_base64=chart_image_base64)


def __get_attribute_comparison_chart_image_base64(attribute_name, playlist_name_1, playlist_name_2,
                                                  attribute_value_to_percentage_1, attribute_value_to_percentage_2):
    plt.title(f"Compare {attribute_name} Distribution")
    plt.xlabel(attribute_name)
    plt.ylabel("Percentage")

    x_labels = []
    y_labels_1 = []
    y_labels_2 = []
    for item_1, item_2 in zip(attribute_value_to_percentage_1, attribute_value_to_percentage_2):
        x_labels.append(item_1["label"])
        y_labels_1.append(item_1["percentage"])
        y_labels_2.append(item_2["percentage"])

    plt.bar(x_labels, y_labels_1, fill=False, linewidth=2, edgecolor="red", label=playlist_name_1)
    plt.bar(x_labels, y_labels_2, fill=False, linewidth=2, edgecolor="blue", label=playlist_name_2)
    plt.xticks(rotation=15)
    plt.legend()
    plt.tight_layout()

    return __get_image_base64_from_plot()


def __get_track_id_from_track_url(track_url):
    start_index = track_url.find("track/") + len("track/")
    end_index = track_url.find("?")

    return track_url[start_index:end_index]
