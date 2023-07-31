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

compare_attribute_distribution_view = Blueprint("compare_attribute_distribution_view", __name__)


@compare_attribute_distribution_view.route(URL_PREFIX + "compare-attribute-distribution-of-playlists", methods=["GET"])
@Utils.measure_execution_time(log_prefix="[View Endpoint] ")
def compare_attribute_distribution_of_playlists():
    try:
        playlist_id_1 = request.args.get("playlist_id_1")
        playlist_id_2 = request.args.get("playlist_id_2")
        attribute = request.args.get("attribute")

        # Just use empty string as fallback if attribute invalid. In this case, API will return an error anyway.
        attribute_display_name = ViewUtils.ATTRIBUTE_DISPLAY_NAMES.get(attribute, "")

        playlist_1 = api_client.get_playlist_by_id(playlist_id_1)
        playlist_2 = api_client.get_playlist_by_id(playlist_id_2)
        attribute_distribution_items_1 = api_client.get_attribute_distribution_of_playlist(playlist_id_1, attribute)
        attribute_distribution_items_2 = api_client.get_attribute_distribution_of_playlist(playlist_id_2, attribute)
        average_value_1 = playlist_1.get_average_value_as_string_for_attribute(attribute)
        average_value_2 = playlist_2.get_average_value_as_string_for_attribute(attribute)

        return __render_compare_attribute_distribution_template(
            playlist_1, playlist_2, attribute_display_name,
            attribute_distribution_items_1, attribute_distribution_items_2,
            average_value_1, average_value_2)
    except HttpError as error:
        return render_template("error.html", error=error), error.status_code
    except Exception:
        error = HttpError.from_last_exception()
        return render_template("error.html", error=error), error.status_code


@Utils.measure_execution_time(log_prefix="compare_attribute_distribution_view.")
def __render_compare_attribute_distribution_template(
        playlist_1, playlist_2, attribute_display_name,
        attribute_distribution_items_1, attribute_distribution_items_2,
        average_value_1, average_value_2):

    chart_image_base64 = __get_attribute_comparison_chart_image_base64(
        attribute_display_name, playlist_1.name, playlist_2.name,
        attribute_distribution_items_1, attribute_distribution_items_2
    )

    return render_template(
        "compare_attribute_distribution.html",
        playlist_1=playlist_1, playlist_2=playlist_2, attribute_display_name=attribute_display_name,
        attribute_distribution_items_1=attribute_distribution_items_1,
        attribute_distribution_items_2=attribute_distribution_items_2,
        chart_image_base64=chart_image_base64,
        average_value_1=average_value_1, average_value_2=average_value_2)


@Utils.measure_execution_time(log_prefix="compare_attribute_distribution_view.")
def __get_attribute_comparison_chart_image_base64(
        attribute_display_name, playlist_name_1, playlist_name_2,
        attribute_value_to_percentage_1, attribute_value_to_percentage_2):

    plt.title(f"Compare {attribute_display_name} Distribution")
    plt.xlabel(attribute_display_name)
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

    return ViewUtils.get_image_base64_from_plot()
