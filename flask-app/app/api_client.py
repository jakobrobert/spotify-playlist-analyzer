from spotify.spotify_playlist import SpotifyPlaylist
from spotify.spotify_track import SpotifyTrack
from http_error import HttpError

import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

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
            track = self.__create_spotify_track(track_data)
            playlist.tracks.append(track)

        return playlist

    def get_attribute_distribution_of_playlist(self, playlist_id, attribute):
        sub_url = f"playlist/{playlist_id}/attribute-distribution"
        request_params = {"attribute": attribute}

        return self.__send_get_request(sub_url, request_params)

    def export_playlist(self):
        sub_url = f"playlist/export"
        response_data = self.__send_post_request(sub_url)

        return response_data["exported_playlist_id"]

    def get_valid_keys(self):
        return self.__send_get_request("valid-keys")

    def get_valid_modes(self):
        return self.__send_get_request("valid-modes")

    def get_valid_key_signatures(self):
        return self.__send_get_request("valid-key-signatures")

    def get_valid_attributes_for_attribute_distribution(self):
        return self.__send_get_request("valid-attributes-for-attribute-distribution")

    def get_track_by_id(self, track_id):
        sub_url = f"track/{track_id}"
        track_data = self.__send_get_request(sub_url)

        return self.__create_spotify_track(track_data)

    def search_tracks(self, query):
        sub_url = f"search-tracks"
        params = {"query": query}
        tracks_data = self.__send_get_request(sub_url, params)

        tracks = []

        for track_data in tracks_data:
            track = self.__create_spotify_track(track_data)
            tracks.append(track)

        return tracks

    def __send_get_request(self, sub_url, params=None):
        url = f"{self.base_url}{sub_url}"
        response = requests.get(url, params=params)
        response_data = response.json()

        if "error" in response_data:
            error = response_data["error"]
            status_code = error["status_code"]
            title = error["title"]
            message = error["message"]
            traceback_items = error["traceback_items"]

            raise HttpError(status_code, title, message, traceback_items)

        return response_data

    def __send_post_request(self, sub_url, data=None):
        url = f"{self.base_url}{sub_url}"
        response = requests.post(url, data=data)
        response_data = response.json()

        if "error" in response_data:
            # TODO same code as in __send_get_request, therefore extract method
            error = response_data["error"]
            status_code = error["status_code"]
            title = error["title"]
            message = error["message"]
            traceback_items = error["traceback_items"]

            raise HttpError(status_code, title, message, traceback_items)

        return response_data

    @staticmethod
    def __create_spotify_track(track_data):
        track = SpotifyTrack()

        track.id = track_data["id"]
        track.title = track_data["title"]
        track.artist_ids = track_data["artist_ids"]
        track.artists = track_data["artists"]
        track.duration_ms = track_data["duration_ms"]
        track.release_year = track_data["release_year"]
        track.popularity = track_data["popularity"]
        track.genres = track_data["genres"]
        track.tempo = track_data["tempo"]
        track.key = track_data["key"]
        track.mode = track_data["mode"]
        track.key_signature = track_data["key_signature"]
        track.camelot = track_data["camelot"]
        track.loudness = track_data["loudness"]

        return track
