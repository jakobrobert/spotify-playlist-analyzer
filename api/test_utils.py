import json

from core.playlist.playlist import Playlist


class TestUtils:
    PLAYLIST_ID_TOP_100 = "26LDpXWgS0nYibyLS9X4Wq"
    PLAYLIST_ID_EMPTY = "40389fDt9evjBgcgIMAlxe"

    @staticmethod
    def load_playlist_from_json_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            playlist_dict = json.load(file)

        return Playlist.from_dict(playlist_dict)

    @staticmethod
    def load__and_validate_top_100_playlist():
        playlist_directory_name = f"{TestUtils.PLAYLIST_ID_TOP_100}_top_100_greatest_songs_of_all_time"
        file_path = f"test_data/playlists/{playlist_directory_name}/playlist.json"
        playlist = TestUtils.load_playlist_from_json_file(file_path)

        # We use assert instead of assertEquals because cannot use it in setUpClass
        assert TestUtils.PLAYLIST_ID_TOP_100 == playlist.id
        assert "Top 100 Greatest Songs of All Time [Backup on 2023-09-15 14:40 UTC]" == playlist.name
        assert 117 == len(playlist.tracks)

        return playlist

    @staticmethod
    def load_and_validate_empty_playlist():
        playlist_directory_name = f"{TestUtils.PLAYLIST_ID_EMPTY}_empty"
        file_path = f"test_data/playlists/{playlist_directory_name}/playlist.json"
        playlist = TestUtils.load_playlist_from_json_file(file_path)

        # We use assert instead of assertEquals because cannot use it in setUpClass
        assert TestUtils.PLAYLIST_ID_EMPTY == playlist.id
        assert "Empty Playlist" == playlist.name
        assert 0 == len(playlist.tracks)

        return playlist
