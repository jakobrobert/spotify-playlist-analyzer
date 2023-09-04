import unittest

from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    def test_playlist_basic_values(self):
        playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json")

        self.assertEqual("6i2Qd6OpeRBAzxfscNXeWp", playlist.id)
        self.assertEqual("Top 100 Greatest Songs of All Time", playlist.name)
        self.assertEqual(117, len(playlist.tracks))

    def test_empty_playlist_basic_values(self):
        playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_40389fDt9evjBgcgIMAlxe_empty.json")

        self.assertEqual("40389fDt9evjBgcgIMAlxe", playlist.id)
        self.assertEqual("Empty Playlist", playlist.name)
        self.assertEqual(0, len(playlist.tracks))

    # TODONOW add 2 tests for each method of PlaylistStatistics. One for top 100 playlist, one for empty one.