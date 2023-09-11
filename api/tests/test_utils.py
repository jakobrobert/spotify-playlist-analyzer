import json

from ..core.playlist.playlist import Playlist


class TestUtils:
    @staticmethod
    def load_playlist_from_json_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            playlist_dict = json.load(file)

        return Playlist.from_dict(playlist_dict)
