from json import JSONDecodeError
import requests

from core.spotify.spotify_playlist import SpotifyPlaylist
from core.spotify.spotify_track import SpotifyTrack
from core.http_error import HttpError
from core.utils import Utils


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_playlist_by_id(self, playlist_id, request_params=None):
        sub_url = f"playlist/{playlist_id}"
        playlist_data = self.__send_get_request(sub_url, request_params)

        playlist = SpotifyPlaylist()
        playlist.id = playlist_data["id"]
        playlist.name = playlist_data["name"]
        playlist.total_duration_ms = playlist_data["total_duration_ms"]
        playlist.average_duration_ms = playlist_data["average_duration_ms"]
        playlist.average_release_year = playlist_data["average_release_year"]
        playlist.average_popularity = playlist_data["average_popularity"]
        playlist.average_tempo = playlist_data["average_tempo"]

        playlist.tracks = []
        for track_data in playlist_data["tracks"]:
            track = ApiClient.__convert_dict_to_track(track_data)
            playlist.tracks.append(track)

        return playlist

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_attribute_distribution_of_playlist(self, playlist_id, attribute):
        sub_url = f"playlist/{playlist_id}/attribute-distribution"
        request_params = {"attribute": attribute}

        return self.__send_get_request(sub_url, request_params)

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def create_playlist(self, playlist_name, track_ids):
        sub_url = f"playlist"
        data = {
            "playlist_name": playlist_name,
            "track_ids": track_ids
        }
        response_data = self.__send_post_request(sub_url, data=data)

        return response_data["playlist_id"]

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_valid_attributes_for_attribute_distribution(self):
        return self.__send_get_request("valid-attributes-for-attribute-distribution")

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_valid_attributes_for_sort_option(self):
        return self.__send_get_request("valid-attributes-for-sort-option")

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_numerical_attributes_for_filter_option(self):
        return self.__send_get_request("numerical-attributes-for-filter-option")

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_valid_keys(self):
        return self.__send_get_request("valid-keys")

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_valid_modes(self):
        return self.__send_get_request("valid-modes")

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_valid_key_signatures(self):
        return self.__send_get_request("valid-key-signatures")

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def get_track_by_id(self, track_id):
        sub_url = f"track/{track_id}"
        track_dict = self.__send_get_request(sub_url)

        return self.__convert_dict_to_track(track_dict)

    @Utils.measure_execution_time(log_prefix="ApiClient.")
    def search_tracks(self, query):
        sub_url = f"search-tracks"
        params = {"query": query}
        tracks_data = self.__send_get_request(sub_url, params)

        tracks = []

        for track_data in tracks_data:
            track = self.__convert_dict_to_track(track_data)
            tracks.append(track)

        return tracks

    def __send_get_request(self, sub_url, params=None):
        url = f"{self.base_url}{sub_url}"
        response = requests.get(url, params=params)

        try:
            response_data = response.json()
            http_error = ApiClient.__create_http_error_from_response_data(response_data)

            if http_error:
                raise http_error

            return response_data
        except JSONDecodeError:
            if "502 Bad Gateway" in response.text:
                raise HttpError(status_code=502, title="API Error", message="Bad Gateway (cannot reach API)")

    def __send_post_request(self, sub_url, data=None):
        url = f"{self.base_url}{sub_url}"
        # Use json=data so the data is encoded as JSON, else would be url encoded
        response = requests.post(url, json=data)

        try:
            response_data = response.json()
            http_error = ApiClient.__create_http_error_from_response_data(response_data)

            if http_error:
                raise http_error

            return response_data
        except JSONDecodeError:
            if "502 Bad Gateway" in response.text:
                raise HttpError(status_code=502, title="API Error", message="Bad Gateway (cannot reach API)")

    @staticmethod
    def __create_http_error_from_response_data(response_data):
        if "error" not in response_data:
            return None

        error = response_data["error"]
        status_code = error["status_code"]
        title = error["title"]
        message = error["message"]
        traceback_items = error["traceback_items"]

        return HttpError(status_code, title, message, traceback_items)

    @staticmethod
    def __convert_dict_to_track(track_dict):
        track = SpotifyTrack()

        track.id = track_dict["id"]
        track.title = track_dict["title"]
        track.artist_ids = track_dict["artist_ids"]
        track.artists = track_dict["artists"]
        track.duration_ms = track_dict["duration_ms"]
        track.release_year = track_dict["release_year"]
        track.popularity = track_dict["popularity"]
        track.genres = track_dict["genres"]

        # Audio Features
        track.tempo = track_dict["tempo"]
        track.key = track_dict["key"]
        track.mode = track_dict["mode"]
        track.key_signature = track_dict["key_signature"]
        track.loudness = track_dict["loudness"]
        track.danceability = track_dict["danceability"]
        track.energy = track_dict["energy"]
        track.valence = track_dict["valence"]
        track.instrumentalness = track_dict["instrumentalness"]
        track.acousticness = track_dict["acousticness"]
        track.liveness = track_dict["liveness"]
        track.speechiness = track_dict["speechiness"]

        return track
