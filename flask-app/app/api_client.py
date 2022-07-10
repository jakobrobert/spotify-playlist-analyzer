from spotify.spotify_playlist import SpotifyPlaylist
from spotify.spotify_track import SpotifyTrack

import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_playlist_by_id(self, playlist_id, request_params=None):
        url = f"{self.base_url}playlist/{playlist_id}"
        response = requests.get(url, params=request_params)
        response_data = response.json()

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
            track.camelot = track_data["camelot"]
            track.loudness = track_data["loudness"]
            playlist.tracks.append(track)

        return playlist

    def get_attribute_distribution_of_playlist(self, playlist_id, attribute):
        url = f"{self.base_url}playlist/{playlist_id}/attribute-distribution"
        request_params = {"attribute": attribute}
        response = requests.get(url, params=request_params)
        response_data = response.json()

        return response_data
