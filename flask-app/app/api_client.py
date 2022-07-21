from spotify.spotify_playlist import SpotifyPlaylist
from spotify.spotify_track import SpotifyTrack
from http_error import HttpError

import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_playlist_by_id(self, playlist_id, request_params=None):
        sub_url = f"playlist/{playlist_id}"
        response_data = self.__send_get_request(sub_url, request_params)

        playlist = SpotifyPlaylist()
        playlist.id = response_data["id"]
        playlist.name = response_data["name"]
        playlist.total_duration_ms = response_data["total_duration_ms"]
        playlist.average_duration_ms = response_data["average_duration_ms"]
        playlist.average_release_year = response_data["average_release_year"]
        playlist.average_tempo = response_data["average_tempo"]

        playlist.tracks = []
        for track_data in response_data["tracks"]:
            track = SpotifyTrack()
            track.id = track_data["id"]
            track.title = track_data["title"]
            track.artist_ids = track_data["artist_ids"]
            track.artists = track_data["artists"]
            track.duration_ms = track_data["duration_ms"]
            track.release_year = track_data["release_year"]
            track.genres = track_data["genres"]
            track.tempo = track_data["tempo"]
            track.key = track_data["key"]
            track.mode = track_data["mode"]
            track.key_signature = track_data["key_signature"]
            track.camelot = track_data["camelot"]
            track.loudness = track_data["loudness"]
            playlist.tracks.append(track)

        return playlist

    def get_attribute_distribution_of_playlist(self, playlist_id, attribute):
        sub_url = f"playlist/{playlist_id}/attribute-distribution"
        request_params = {"attribute": attribute}

        return self.__send_get_request(sub_url, request_params)

    def get_valid_keys(self):
        return self.__send_get_request("valid-keys")

    def get_valid_modes(self):
        return self.__send_get_request("valid-modes")

    def get_valid_key_signatures(self):
        return self.__send_get_request("valid-key-signatures")

    def __send_get_request(self, sub_url, request_params=None):
        url = f"{self.base_url}{sub_url}"
        response = requests.get(url, request_params)
        response_data = response.json()

        if "error" in response_data:
            error = response_data["error"]
            status = error["status_code"]
            message = error["message"]

            raise HttpError(status, message)

        return response_data
