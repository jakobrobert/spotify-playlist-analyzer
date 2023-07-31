from core.api_client import ApiClient
from core.http_error import HttpError
from core.views.view_utils import ViewUtils
from core.utils import Utils

from flask import Blueprint, render_template, request
import configparser
import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
API_BASE_URL = config["DEFAULT"]["API_BASE_URL"]

api_client = ApiClient(API_BASE_URL)

attribute_distribution_view = Blueprint("attribute_distribution_view", __name__)


@attribute_distribution_view.route(URL_PREFIX + "playlist/<playlist_id>/attribute-distribution", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
def get_attribute_distribution_of_playlist(playlist_id):
    try:
        attribute = request.args.get("attribute")

        # Just use empty string as fallback if attribute invalid. In this case, API will return an error anyway.
        attribute_display_name = ViewUtils.ATTRIBUTE_DISPLAY_NAMES.get(attribute, "")
        playlist = api_client.get_playlist_by_id(playlist_id)
        attribute_distribution_items = api_client.get_attribute_distribution_of_playlist(playlist_id, attribute)
        average_value = playlist.get_average_value_as_string_for_attribute(attribute)

        return __render_attribute_distribution_template(
            playlist, attribute_display_name, attribute_distribution_items, average_value)
    except HttpError as error:
        return render_template("error.html", error=error), error.status_code
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error), error.status_code


@Utils.measure_execution_time(log_prefix="attribute_distribution_view.")
def __render_attribute_distribution_template(
        playlist, attribute_display_name, attribute_distribution_items, average_value):

    histogram_image_base64 = __get_histogram_image_base64(attribute_display_name, attribute_distribution_items)

    return render_template(
        "attribute_distribution.html", playlist=playlist, attribute_display_name=attribute_display_name,
        attribute_distribution_items=attribute_distribution_items, histogram_image_base64=histogram_image_base64,
        average_value=average_value)


@Utils.measure_execution_time(log_prefix="attribute_distribution_view.")
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
