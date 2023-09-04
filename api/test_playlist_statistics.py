import unittest

from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.top_100_playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json")
        self.empty_playlist = TestUtils.load_playlist_from_json_string(
            "./test_data/playlist_40389fDt9evjBgcgIMAlxe_empty.json")

    def tearDown(self):
        pass

    def test_playlist_basic_values(self):
        # TODONOW assert id, name, number of tracks
        pass

    def test_empty_playlist_basic_values(self):
        # TODONOW assert id, name, number of tracks
        pass

    # TODONOW add 2 tests for each method of PlaylistStatistics. One for top 100 playlist, one for empty one.