import matplotlib.pyplot as plt
from io import BytesIO
import base64


class ViewUtils:
    ATTRIBUTE_DISPLAY_NAMES = {
        "artists": "Artists",
        "title": "Title",
        "duration_ms": "Duration",
        "release_year": "Release Year",
        "popularity": "Popularity",
        "genres": "Genres",

        # Audio Features
        "tempo": "Tempo (BPM)",
        "key": "Key",
        "mode": "Mode",
        "key_signature": "Key Signature",
        "camelot": "Camelot",
        "loudness": "Loudness (dB)",
        "danceability": "Danceablity",
        "energy": "Energy",
        "speechiness": "Speechiness",
        "acousticness": "Acousticness",
        "instrumentalness": "Instrumentalness",
        "liveness": "Liveness",
        "valence": "Valence"
    }

    NUMERICAL_ATTRIBUTES_TO_FILTER_BY = [
        "tempo", "release_year"
    ]

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

    @staticmethod
    def get_image_base64_from_plot():
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format="png")
        plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
        image_bytes = image_buffer.getvalue()
        image_base64_bytes = base64.encodebytes(image_bytes)
        image_base64_string = image_base64_bytes.decode("utf8")

        return image_base64_string
