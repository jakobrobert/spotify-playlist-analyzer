import unittest

from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # TODONOW load json from file
        playlist_json = ""
        self.top_100_playlist = TestUtils.load_playlist_from_json_string(playlist_json)
        empty_playlist_json = ""
        self.empty_playlist = TestUtils.load_playlist_from_json_string(empty_playlist_json)
        pass

    def tearDown(self):
        pass

    def test_playlist_basic_values(self):
        # TODONOW assert id, name, number of tracks
        pass

    def test_empty_playlist_basic_values(self):
        # TODONOW assert id, name, number of tracks
        pass

    # TODONOW add 2 tests for each method of PlaylistStatistics. One for top 100 playlist, one for empty one.