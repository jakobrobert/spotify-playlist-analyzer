import unittest

from core.analysis.playlist_statistics import PlaylistStatistics
from test_utils import TestUtils

NORMAL_PLAYLIST_FILE_PATH = "./test_data/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json"
EMPTY_PLAYLIST_FILE_PATH = "./test_data/playlist_40389fDt9evjBgcgIMAlxe_empty.json"


class MyTestCase(unittest.TestCase):
    def test_normal_playlist_basic_values(self):
        playlist = TestUtils.load_playlist_from_json_file(NORMAL_PLAYLIST_FILE_PATH)

        self.assertEqual("6i2Qd6OpeRBAzxfscNXeWp", playlist.id)
        self.assertEqual("Top 100 Greatest Songs of All Time", playlist.name)
        self.assertEqual(117, len(playlist.tracks))

    def test_empty_playlist_basic_values(self):
        playlist = TestUtils.load_playlist_from_json_file(EMPTY_PLAYLIST_FILE_PATH)

        self.assertEqual("40389fDt9evjBgcgIMAlxe", playlist.id)
        self.assertEqual("Empty Playlist", playlist.name)
        self.assertEqual(0, len(playlist.tracks))

    # TODONOW add 2 tests for each method of PlaylistStatistics. One for top 100 playlist, one for empty one.
    def test_normal_playlist_total_duration(self):
        playlist = TestUtils.load_playlist_from_json_file(NORMAL_PLAYLIST_FILE_PATH)
        statistics = PlaylistStatistics(playlist.tracks)

        self.assertEqual(28022939, statistics.get_total_duration_ms())

    def test_empty_playlist_total_duration(self):
        playlist = TestUtils.load_playlist_from_json_file(EMPTY_PLAYLIST_FILE_PATH)
        statistics = PlaylistStatistics(playlist.tracks)

        self.assertEqual(0, statistics.get_total_duration_ms())
