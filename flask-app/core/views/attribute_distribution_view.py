from app.api_client import ApiClient
from http_error import HttpError
from views.view_utils import ViewUtils

from flask import Blueprint, render_template, request
import configparser
import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read("../config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

attribute_distribution_view = Blueprint("attribute_distribution_view", __name__)


@attribute_distribution_view.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
def get_attribute_distribution_of_playlist(playlist_id):
    try:
        attribute = request.args.get("attribute")

        # Just use "" as fallback if attribute invalid. In this case, API will return an error anyway.
        attribute_display_name = ViewUtils.ATTRIBUTE_DISPLAY_NAMES.get(attribute, "")
        playlist = api_client.get_playlist_by_id(playlist_id)
        attribute_distribution_items = api_client.get_attribute_distribution_of_playlist(playlist_id, attribute)

        return __render_attribute_distribution_template(playlist, attribute_display_name, attribute_distribution_items)
    except HttpError as error:
        return render_template("error.html", error=error)
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error)


def __render_attribute_distribution_template(playlist, attribute_display_name, attribute_distribution_items):
    histogram_image_base64 = __get_histogram_image_base64(attribute_display_name, attribute_distribution_items)

    return render_template("attribute_distribution.html", playlist=playlist,
                           attribute_display_name=attribute_display_name,
                           attribute_distribution_items=attribute_distribution_items,
                           histogram_image_base64=histogram_image_base64)


def __get_histogram_image_base64(attribute_display_name, attribute_value_to_percentage):
    plt.title(f"{attribute_display_name} Distribution")
    plt.xlabel(attribute_display_name)
    plt.ylabel("Percentage")

    x_labels = []
    y_labels = []
    for item in attribute_value_to_percentage:
        x_labels.append(item["label"])
        y_labels.append(item["percentage"])

    plt.bar(x_labels, y_labels, edgecolor="black")
    plt.xticks(rotation=15)
    plt.tight_layout()

    return ViewUtils.get_image_base64_from_plot()
