import json

from core.playlist.playlist import Playlist
from core.playlist.track import Track


class TestUtils:
    @staticmethod
    def load_playlist_from_json_string(json_string):
        playlist = Playlist()

        # TODONOW FIX fails with JSONDecodeError
        playlist_dict = json.loads(json_string)
        playlist.id = playlist_dict["id"]
        playlist.name = playlist_dict["name"]

        tracks_dict = playlist_dict["tracks"]

        playlist.tracks = []
        for track_dict in tracks_dict:
            track = Track()
            # TODONOW get all attribute values for Track from dict
            playlist.tracks.append(track)

        return playlist

    @staticmethod
    def load_playlist_from_json_file(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_string = file.read()

            return TestUtils.load_playlist_from_json_string(json_string)
        except FileNotFoundError as e:
            print(f"load_playlist_from_json_file failed: file_path: '{file_path}', e: {e}")

