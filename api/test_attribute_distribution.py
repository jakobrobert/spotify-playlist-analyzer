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
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("duration_ms")
        actual_items = self.top_100_playlist_attribute_distribution.get_duration_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_duration_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("duration_ms")
        actual_items = self.empty_playlist_attribute_distribution.get_duration_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_top_100_playlist_release_year_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("release_year")
        actual_items = self.top_100_playlist_attribute_distribution.get_release_year_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_release_year_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("release_year")
        actual_items = self.empty_playlist_attribute_distribution.get_release_year_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_top_100_playlist_popularity_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("popularity")
        actual_items = self.top_100_playlist_attribute_distribution.get_popularity_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_popularity_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("popularity")
        actual_items = self.empty_playlist_attribute_distribution.get_popularity_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_top_100_playlist_super_genres_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("super_genres")
        actual_items = self.top_100_playlist_attribute_distribution.get_super_genres_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_super_genres_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("super_genres")
        actual_items = self.empty_playlist_attribute_distribution.get_super_genres_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_top_100_playlist_tempo_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("tempo")
        actual_items = self.top_100_playlist_attribute_distribution.get_tempo_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_tempo_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("tempo")
        actual_items = self.empty_playlist_attribute_distribution.get_tempo_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_key_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("key")
        actual_items = self.top_100_playlist_attribute_distribution.get_key_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_key_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("key")
        actual_items = self.empty_playlist_attribute_distribution.get_key_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_mode_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("mode")
        actual_items = self.top_100_playlist_attribute_distribution.get_mode_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_mode_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("mode")
        actual_items = self.empty_playlist_attribute_distribution.get_mode_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_key_and_mode_pair_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("key_and_mode_pair")
        actual_items = self.top_100_playlist_attribute_distribution.get_key_and_mode_pair_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_key_and_mode_pair_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("key_and_mode_pair")
        actual_items = self.empty_playlist_attribute_distribution.get_key_and_mode_pair_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_key_signature_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("key_signature")
        actual_items = self.top_100_playlist_attribute_distribution.get_key_signature_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_key_signature_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("key_signature")
        actual_items = self.empty_playlist_attribute_distribution.get_key_signature_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_top_100_playlist_loudness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("loudness")
        actual_items = self.top_100_playlist_attribute_distribution.get_loudness_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_loudness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("loudness")
        actual_items = self.empty_playlist_attribute_distribution.get_loudness_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_danceability_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("danceability")
        actual_items = self.top_100_playlist_attribute_distribution.get_danceability_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_danceability_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("danceability")
        actual_items = self.empty_playlist_attribute_distribution.get_danceability_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_energy_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("energy")
        actual_items = self.top_100_playlist_attribute_distribution.get_energy_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_energy_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("energy")
        actual_items = self.empty_playlist_attribute_distribution.get_energy_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_speechiness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("speechiness")
        actual_items = self.top_100_playlist_attribute_distribution.get_speechiness_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_speechiness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("speechiness")
        actual_items = self.empty_playlist_attribute_distribution.get_speechiness_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_liveness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("liveness")
        actual_items = self.top_100_playlist_attribute_distribution.get_liveness_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_liveness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("liveness")
        actual_items = self.empty_playlist_attribute_distribution.get_liveness_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_acousticness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("acousticness")
        actual_items = self.top_100_playlist_attribute_distribution.get_acousticness_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_acousticness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("acousticness")
        actual_items = self.empty_playlist_attribute_distribution.get_acousticness_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_instrumentalness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("instrumentalness")
        actual_items = self.top_100_playlist_attribute_distribution.get_instrumentalness_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_instrumentalness_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("instrumentalness")
        actual_items = self.empty_playlist_attribute_distribution.get_instrumentalness_items()
        self.__assert_distribution_items(actual_items, expected_items)
        
    def test_top_100_playlist_valence_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_top_100_playlist("valence")
        actual_items = self.top_100_playlist_attribute_distribution.get_valence_items()
        self.__assert_distribution_items(actual_items, expected_items)

    def test_empty_playlist_valence_distribution(self):
        expected_items = self.__load_expected_distribution_items_for_empty_playlist("valence")
        actual_items = self.empty_playlist_attribute_distribution.get_valence_items()
        self.__assert_distribution_items(actual_items, expected_items)

    @staticmethod
    def __load__and_validate_top_100_playlist():
        playlist_id = "26LDpXWgS0nYibyLS9X4Wq"
        file_path = f"test_data/playlists/playlist_{playlist_id}_top_100_greatest_songs_of_all_time.json"
        playlist = TestUtils.load_playlist_from_json_file(file_path)

        # Note: We use assert instead of assertEquals because cannot use it in setUpClass
        assert "26LDpXWgS0nYibyLS9X4Wq" == playlist.id
        assert "Top 100 Greatest Songs of All Time [Backup on 2023-09-15 14:40 UTC]" == playlist.name
        assert 117 == len(playlist.tracks)

        return playlist

    @staticmethod
    def __load_and_validate_empty_playlist():
        playlist_id = "40389fDt9evjBgcgIMAlxe"
        file_path = f"test_data/playlists/playlist_{playlist_id}_empty.json"
        playlist = TestUtils.load_playlist_from_json_file(file_path)

        # Note: We use assert instead of assertEquals because cannot use it in setUpClass
        assert playlist_id == playlist.id
        assert "Empty Playlist" == playlist.name
        assert 0 == len(playlist.tracks)

        return playlist

    @staticmethod
    def __load_expected_distribution_items(playlist_id, attribute_name):
        file_path_prefix = "test_data/attribute_distribution/attribute_distribution_of_playlist"
        file_path = f"{file_path_prefix}_{playlist_id}_{attribute_name}.json"

        with open(file_path, "r", encoding="utf-8") as file:
            expected_items = json.load(file)

        return expected_items

    @staticmethod
    def __load_expected_distribution_items_for_top_100_playlist(attribute_name):
        playlist_id = "26LDpXWgS0nYibyLS9X4Wq"
        return TestAttributeDistribution.__load_expected_distribution_items(playlist_id, attribute_name)

    @staticmethod
    def __load_expected_distribution_items_for_empty_playlist(attribute_name):
        playlist_id = "40389fDt9evjBgcgIMAlxe"
        return TestAttributeDistribution.__load_expected_distribution_items(playlist_id, attribute_name)

    def __assert_distribution_items(self, actual_items, expected_items):
        self.assertEqual(len(expected_items), len(actual_items))

        for expected_item, actual_item in zip(expected_items, actual_items):
            self.assertEqual(expected_item["label"], actual_item["label"])
            self.assertEqual(expected_item["count"], actual_item["count"])
            self.assertEqual(expected_item["percentage"], actual_item["percentage"])
