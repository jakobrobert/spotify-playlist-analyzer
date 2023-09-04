from core.playlist.playlist import Playlist


class TestUtils:
    @staticmethod
    def load_playlist_from_json_string(json_string):
        playlist = Playlist()

        # TODONOW get dict from json

        # TODONOW get basic data from dict

        tracks = []
        # TODONOW get tracks from dict

        playlist.tracks = tracks

        return playlist

    @staticmethod
    def load_playlist_from_json_file(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_string = file.read()

            return TestUtils.load_playlist_from_json_string(json_string)
        except FileNotFoundError as e:
            print(f"load_playlist_from_json_file failed: file_path: '{file_path}', e: {e}")

