import json

from core.playlist.playlist import Playlist


class TestUtils:
    TOP_100_PLAYLIST_ID = "4PEUZYZ3RoKEcZQoGqu5mV"
    TOP_100_PLAYLIST_DIRECTORY_NAME = f"{TOP_100_PLAYLIST_ID}_top_100_greatest_songs_of_all_time"

    EMPTY_PLAYLIST_ID = "40389fDt9evjBgcgIMAlxe"
    EMPTY_PLAYLIST_DIRECTORY_NAME = f"{EMPTY_PLAYLIST_ID}_empty"

    @staticmethod
    def load_playlist_from_json_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            playlist_dict = json.load(file)

        return Playlist.from_dict(playlist_dict)

    @staticmethod
    def load__and_validate_top_100_playlist():
        file_path = f"test_data/playlists/{TestUtils.TOP_100_PLAYLIST_DIRECTORY_NAME}/playlist.json"
        playlist = TestUtils.load_playlist_from_json_file(file_path)

        # We use assert instead of assertEquals because cannot use it in setUpClass
        assert TestUtils.TOP_100_PLAYLIST_ID == playlist.id
        assert "Top 100 Greatest Songs of All Time [Backup on 2023-09-22 15:20 UTC]" == playlist.name
        assert 117 == len(playlist.tracks)

        return playlist

    @staticmethod
    def load_and_validate_empty_playlist():
        file_path = f"test_data/playlists/{TestUtils.EMPTY_PLAYLIST_DIRECTORY_NAME}/playlist.json"
        playlist = TestUtils.load_playlist_from_json_file(file_path)

        # We use assert instead of assertEquals because cannot use it in setUpClass
        assert TestUtils.EMPTY_PLAYLIST_ID == playlist.id
        assert "Empty Playlist" == playlist.name
        assert 0 == len(playlist.tracks)

        return playlist
