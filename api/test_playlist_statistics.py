# WARNING Keep tests in root directory. Tried to move into "tests" directory,
# Got tests & dev working by using relative imports, but this broke uat / uwsgi. See #317

import unittest

from core.analysis.playlist_statistics import PlaylistStatistics
from test_utils import TestUtils


class TestPlaylistStatistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        top_100_playlist = TestUtils.load_and_validate_top_100_playlist()
        cls.top_100_playlist_statistics = PlaylistStatistics(top_100_playlist.tracks)

        empty_playlist = TestUtils.load_and_validate_empty_playlist()
        cls.empty_playlist_statistics = PlaylistStatistics(empty_playlist.tracks)

    def test_top_100_playlist_total_duration(self):
        self.assertEqual(28014935, self.top_100_playlist_statistics.get_total_duration_ms())

    def test_empty_playlist_total_duration(self):
        self.assertEqual(0, self.empty_playlist_statistics.get_total_duration_ms())

    def test_top_100_playlist_average_duration(self):
        self.assertAlmostEqual(239444, self.top_100_playlist_statistics.get_average_duration_ms(), 0)

    def test_empty_playlist_average_duration(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_duration_ms())

    def test_top_100_playlist_average_popularity(self):
        self.assertAlmostEqual(65, self.top_100_playlist_statistics.get_average_popularity(), 0)

    def test_empty_playlist_average_popularity(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_popularity())
        
    def test_top_100_playlist_average_release_year(self):
        self.assertAlmostEqual(1987, self.top_100_playlist_statistics.get_average_release_year(), 0)

    def test_empty_playlist_average_release_year(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_release_year())
        
    def test_top_100_playlist_average_tempo(self):
        self.assertAlmostEqual(118, self.top_100_playlist_statistics.get_average_tempo(), 0)

    def test_empty_playlist_average_tempo(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_tempo())
        
    def test_top_100_playlist_average_speechiness(self):
        self.assertAlmostEqual(5, self.top_100_playlist_statistics.get_average_speechiness(), 0)

    def test_empty_playlist_average_speechiness(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_speechiness())
        
    def test_top_100_playlist_average_liveness(self):
        self.assertAlmostEqual(19, self.top_100_playlist_statistics.get_average_liveness(), 0)

    def test_empty_playlist_average_liveness(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_liveness())

    def test_top_100_playlist_average_acousticness(self):
        self.assertAlmostEqual(27, self.top_100_playlist_statistics.get_average_acousticness(), 0)

    def test_empty_playlist_average_acousticness(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_acousticness())

    def test_top_100_playlist_average_instrumentalness(self):
        self.assertAlmostEqual(1, self.top_100_playlist_statistics.get_average_instrumentalness(), 0)

    def test_empty_playlist_average_instrumentalness(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_instrumentalness())

    def test_top_100_playlist_average_valence(self):
        self.assertAlmostEqual(62, self.top_100_playlist_statistics.get_average_valence(), 0)

    def test_empty_playlist_average_valence(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_valence())

    def test_top_100_playlist_average_energy(self):
        self.assertAlmostEqual(62, self.top_100_playlist_statistics.get_average_energy(), 0)

    def test_empty_playlist_average_energy(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_energy())

    def test_top_100_playlist_average_danceability(self):
        self.assertAlmostEqual(58, self.top_100_playlist_statistics.get_average_danceability(), 0)

    def test_empty_playlist_average_danceability(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_danceability())
