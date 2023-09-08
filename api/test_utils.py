import json

from core.playlist.playlist import Playlist
from core.playlist.track import Track


class TestUtils:
    @staticmethod
    def load_playlist_from_json_string(json_string):
        playlist = Playlist()

        playlist_dict = json.loads(json_string)
        playlist.id = playlist_dict["id"]
        playlist.name = playlist_dict["name"]

        tracks_dict = playlist_dict["tracks"]

        playlist.tracks = []
        for track_dict in tracks_dict:
            track = Track()
            
            track.id = track_dict["id"]
            track.artist_ids = track_dict["artist_ids"]
            track.artists = track_dict["artists"]
            track.title = track_dict["title"]
            track.added_by_user_id = track_dict["added_by_user_id"]
            track.added_by = track_dict["added_by"]
            track.duration_ms = track_dict["duration_ms"]
            track.release_year = track_dict["release_year"]
            track.popularity = track_dict["popularity"]
            track.genres = track_dict["genres"]
            track.super_genres = track_dict["super_genres"]
            track.tempo = track_dict["tempo"]
            track.key = track_dict["key"]
            track.mode = track_dict["mode"]
            track.key_and_mode_pair = track_dict["key_and_mode_pair"]
            track.key_signature = track_dict["key_signature"]
            track.loudness = track_dict["loudness"]
            track.danceability = track_dict["danceability"]
            track.energy = track_dict["energy"]
            track.valence = track_dict["valence"]
            track.instrumentalness = track_dict["instrumentalness"]
            track.acousticness = track_dict["acousticness"]
            track.liveness = track_dict["liveness"]
            track.speechiness = track_dict["speechiness"]
            
            playlist.tracks.append(track)

        return playlist

    @staticmethod
    def load_playlist_from_json_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            json_string = file.read()

        return TestUtils.load_playlist_from_json_string(json_string)

