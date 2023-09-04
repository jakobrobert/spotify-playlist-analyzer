import unittest

from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    def test_playlist_basic_values(self):
        playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json")

        self.assertEqual("", playlist.id)
        # TODONOW assert id, name, number of tracks
        pass

    def test_empty_playlist_basic_values(self):
        playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_40389fDt9evjBgcgIMAlxe_empty.json")

        # TODONOW assert id, name, number of tracks
        pass

    # TODONOW add 2 tests for each method of PlaylistStatistics. One for top 100 playlist, one for empty one.