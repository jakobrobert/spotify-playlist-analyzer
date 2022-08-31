import matplotlib.pyplot as plt
from io import BytesIO
import base64


class ViewUtils:
    @staticmethod
    def get_playlist_id_from_playlist_url(playlist_url):
        start_index = playlist_url.find("playlist/") + len("playlist/")
        end_index = playlist_url.find("?")

        return playlist_url[start_index:end_index]

    @staticmethod
    def get_attribute_display_name(attribute_name, api_client):
        attributes = api_client.get_valid_attributes_for_attribute_distribution()

        for attribute in attributes:
            if attribute["name"] == attribute_name:
                return attribute["display_name"]

        raise ValueError(f"Invalid attribute: '{attribute_name}'")

    @staticmethod
    def get_image_base64_from_plot():
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format="png")
        plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
        image_bytes = image_buffer.getvalue()
        image_base64_bytes = base64.encodebytes(image_bytes)
        image_base64_string = image_base64_bytes.decode("utf8")

        return image_base64_string
