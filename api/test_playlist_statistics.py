import unittest

from core.analysis.playlist_statistics import PlaylistStatistics
from test_utils import TestUtils


class TestPlaylistStatistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.top_100_playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json"
        )
        cls.empty_playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_40389fDt9evjBgcgIMAlxe_empty.json"
        )

    def test_top_100_playlist_basic_values(self):
        self.assertEqual("6i2Qd6OpeRBAzxfscNXeWp", self.top_100_playlist.id)
        self.assertEqual("Top 100 Greatest Songs of All Time", self.top_100_playlist.name)
        self.assertEqual(117, len(self.top_100_playlist.tracks))

    def test_empty_playlist_basic_values(self):
        self.assertEqual("40389fDt9evjBgcgIMAlxe", self.empty_playlist.id)
        self.assertEqual("Empty Playlist", self.empty_playlist.name)
        self.assertEqual(0, len(self.empty_playlist.tracks))

    # TODONOW add 2 tests for each method of PlaylistStatistics. One for top 100 playlist, one for empty one.
    def test_top_100_playlist_total_duration(self):
        statistics = PlaylistStatistics(self.top_100_playlist.tracks)

        self.assertEqual(28022939, statistics.get_total_duration_ms())

    def test_empty_playlist_total_duration(self):
        statistics = PlaylistStatistics(self.empty_playlist.tracks)

        self.assertEqual(0, statistics.get_total_duration_ms())

    def test_top_100_playlist_average_duration(self):
        statistics = PlaylistStatistics(self.top_100_playlist.tracks)

        self.assertAlmostEqual(239512, statistics.get_average_duration_ms(), 0)

    def test_empty_playlist_average_duration(self):
        statistics = PlaylistStatistics(self.empty_playlist.tracks)

        self.assertEqual(None, statistics.get_average_duration_ms())
