# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from app.http_error import HttpError' is shown as valid locally, but does not work with the server
from http_error import HttpError

import matplotlib.pyplot as plt
from io import BytesIO
import base64


class ViewUtils:
    ATTRIBUTE_DISPLAY_NAMES = {
        "artists": "Artists",
        "title": "Title",
        "duration_ms": "Duration",
        # TODO add remaining attributes
    }

    @staticmethod
    def get_playlist_id_from_playlist_url(playlist_url):
        url_prefix = "playlist/"
        url_prefix_start_index = playlist_url.find(url_prefix)

        if url_prefix_start_index == -1:
            raise ValueError(f"Invalid URL for Spotify Playlist, missing \"{url_prefix}\": {playlist_url}")

        id_start_index = playlist_url.find(url_prefix) + len(url_prefix)
        id_end_index = None

        si_start_index = playlist_url.find("?si=")
        if si_start_index != -1:
            id_end_index = si_start_index

        return playlist_url[id_start_index:id_end_index]

    @staticmethod
    def get_track_id_from_track_url(track_url):
        url_prefix = "track/"
        url_prefix_start_index = track_url.find(url_prefix)

        if url_prefix_start_index == -1:
            raise ValueError(f"Invalid URL for Spotify Track, missing \"{url_prefix}\": {track_url}")

        id_start_index = track_url.find(url_prefix) + len(url_prefix)
        id_end_index = None

        si_start_index = track_url.find("?si=")
        if si_start_index != -1:
            id_end_index = si_start_index

        return track_url[id_start_index:id_end_index]

    # TODO get rid of this method, just pass this constant directly to template, then use it as in playlist template
    @staticmethod
    def get_attribute_display_name(attribute_name):
        if attribute_name not in ViewUtils.ATTRIBUTE_DISPLAY_NAMES:
            raise HttpError(status_code=400, title="Bad Request", message=f"Invalid attribute: '{attribute_name}'")

        return ViewUtils.ATTRIBUTE_DISPLAY_NAMES[attribute_name]

    @staticmethod
    def get_image_base64_from_plot():
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format="png")
        plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
        image_bytes = image_buffer.getvalue()
        image_base64_bytes = base64.encodebytes(image_bytes)
        image_base64_string = image_base64_bytes.decode("utf8")

        return image_base64_string
