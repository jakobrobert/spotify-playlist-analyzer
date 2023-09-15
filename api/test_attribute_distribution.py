# WARNING Keep tests in root directory. Tried to move into "tests" directory,
# Got tests & dev working by using relative imports, but this broke uat / uwsgi. See #317
import json
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

    def test_top_100_playlist_duration_distribution(self):
        # TODONOW extract method to load attribute distribution, pass playlist id & attribute_name, then build file path
        file_path = "test_data/attribute_distribution/attribute_distribution_of_playlist_26LDpXWgS0nYibyLS9X4Wq_duration_ms.json"
        with open(file_path, "r", encoding="utf-8") as file:
            expected_items = json.load(file)

        actual_items = self.top_100_playlist_attribute_distribution.get_duration_items()

        # TODONOW extract method for assertions, can do it generally, independent of attribute
        self.assertEqual(len(expected_items), len(actual_items))

        for expected_item, actual_item in zip(expected_items, actual_items):
            self.assertEqual(expected_item["label"], actual_item["label"])
            self.assertEqual(expected_item["count"], actual_item["count"])
            self.assertEqual(expected_item["percentage"], actual_item["percentage"])

    def test_empty_playlist_duration_distribution(self):
        # TODONOW extract method to load attribute distribution, pass playlist id & attribute_name, then build file path
        file_path = "test_data/attribute_distribution/attribute_distribution_of_playlist_40389fDt9evjBgcgIMAlxe_duration_ms.json"
        with open(file_path, "r", encoding="utf-8") as file:
            expected_items = json.load(file)

        actual_items = self.empty_playlist_attribute_distribution.get_duration_items()

        # TODONOW extract method for assertions, can do it generally, independent of attribute
        self.assertEqual(len(expected_items), len(actual_items))

        for expected_item, actual_item in zip(expected_items, actual_items):
            self.assertEqual(expected_item["label"], actual_item["label"])
            self.assertEqual(expected_item["count"], actual_item["count"])
            self.assertEqual(expected_item["percentage"], actual_item["percentage"])


    # TODONOW Add 2 tests for each method of AttributeDistribution. 1 for top 100, 1 for empty playlist

    @staticmethod
    def __load__and_validate_top_100_playlist():
        path = "test_data/playlists/playlist_26LDpXWgS0nYibyLS9X4Wq_top_100_greatest_songs_of_all_time.json"
        top_100_playlist = TestUtils.load_playlist_from_json_file(path)

        # Note: We use assert instead of assertEquals because cannot use it in setUpClass
        assert "26LDpXWgS0nYibyLS9X4Wq" == top_100_playlist.id
        assert "Top 100 Greatest Songs of All Time [Backup on 2023-09-15 14:40 UTC]" == top_100_playlist.name
        assert 117 == len(top_100_playlist.tracks)
        return top_100_playlist

    @staticmethod
    def __load_and_validate_empty_playlist():
        path = "test_data/playlists/playlist_40389fDt9evjBgcgIMAlxe_empty.json"
        empty_playlist = TestUtils.load_playlist_from_json_file(path)

        # Note: We use assert instead of assertEquals because cannot use it in setUpClass
        assert "40389fDt9evjBgcgIMAlxe" == empty_playlist.id
        assert "Empty Playlist" == empty_playlist.name
        assert 0 == len(empty_playlist.tracks)
        return empty_playlist
