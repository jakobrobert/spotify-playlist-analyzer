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
