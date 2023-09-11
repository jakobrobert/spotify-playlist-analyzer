# WARNING Keep tests in root directory. Tried to move into "tests" directory,
# Got tests & dev working by using relative imports, but this broke uat / uwsgi. See #317

import unittest

from core.analysis.attribute_distribution import AttributeDistribution
from test_utils import TestUtils


class TestAttributeDistribution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        top_100_playlist = cls.__load__and_validate_top_100_playlist()
        cls.top_100_playlist_attribute_distribution = AttributeDistribution(top_100_playlist.tracks)

        empty_playlist = cls.__load_and_validate_empty_playlist()
        cls.empty_playlist_attribute_distribution = AttributeDistribution(empty_playlist.tracks)

    # TODONOW Add 2 tests for each method of AttributeDistribution. 1 for top 100, 1 for empty playlist
    def test_top_100_playlist_duration_distribution(self):
        duration_distribution_items = self.top_100_playlist_attribute_distribution.get_duration_items()

        self.assertEqual(8, len(duration_distribution_items))

        self.assertEqual("< 02:00", duration_distribution_items[0]["label"])
        self.assertEqual(1, duration_distribution_items[0]["count"])
        self.assertAlmostEqual(0.9, duration_distribution_items[0]["percentage"], 1)

        self.assertEqual("≥ 02:00", duration_distribution_items[1]["label"])
        self.assertEqual(12, duration_distribution_items[1]["count"])
        self.assertAlmostEqual(10.3, duration_distribution_items[1]["percentage"], 1)

        # TODONOW better load expected values from json, would be too much work and not maintainable to hardcode everything
        """
        self.assertEqual("≥ 02:30", duration_distribution_items[2]["label"])
        self.assertEqual(1, duration_distribution_items[2]["count"])
        self.assertIsNone(duration_distribution_items[2]["percentage"])

        self.assertEqual("≥ 03:00", duration_distribution_items[3]["label"])
        self.assertEqual(1, duration_distribution_items[3]["count"])
        self.assertIsNone(duration_distribution_items[3]["percentage"])

        self.assertEqual("≥ 03:30", duration_distribution_items[4]["label"])
        self.assertEqual(1, duration_distribution_items[4]["count"])
        self.assertIsNone(duration_distribution_items[4]["percentage"])

        self.assertEqual("≥ 04:00", duration_distribution_items[5]["label"])
        self.assertEqual(1, duration_distribution_items[5]["count"])
        self.assertIsNone(duration_distribution_items[5]["percentage"])

        self.assertEqual("≥ 04:30", duration_distribution_items[6]["label"])
        self.assertEqual(1, duration_distribution_items[6]["count"])
        self.assertIsNone(duration_distribution_items[6]["percentage"])

        self.assertEqual("≥ 05:00", duration_distribution_items[7]["label"])
        self.assertEqual(1, duration_distribution_items[7]["count"])
        self.assertIsNone(duration_distribution_items[7]["percentage"])
        """

    @classmethod
    def __load__and_validate_top_100_playlist(cls):
        path = "test_data/playlists/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json"
        top_100_playlist = TestUtils.load_playlist_from_json_file(path)

        # Note: We use assert instead of assertEquals because cannot use it in setUpClass
        assert "6i2Qd6OpeRBAzxfscNXeWp" == top_100_playlist.id
        assert "Top 100 Greatest Songs of All Time" == top_100_playlist.name
        assert 117 == len(top_100_playlist.tracks)
        return top_100_playlist

    @classmethod
    def __load_and_validate_empty_playlist(cls):
        path = "test_data/playlists/playlist_40389fDt9evjBgcgIMAlxe_empty.json"
        empty_playlist = TestUtils.load_playlist_from_json_file(path)

        # Note: We use assert instead of assertEquals because cannot use it in setUpClass
        assert "40389fDt9evjBgcgIMAlxe" == empty_playlist.id
        assert "Empty Playlist" == empty_playlist.name
        assert 0 == len(empty_playlist.tracks)
        return empty_playlist
