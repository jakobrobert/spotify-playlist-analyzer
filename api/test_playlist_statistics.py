import unittest

from core.analysis.playlist_statistics import PlaylistStatistics
from test_utils import TestUtils


class TestPlaylistStatistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # TODONOW fix assertions, incorrect on purpose to ensure they can fail
        # TODONOW make playlist objects as local var only
        # TODONOW extract methods load_top_100_playlist, load_empty_playlist
        cls.top_100_playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_6i2Qd6OpeRBAzxfscNXeWp_top_100_greatest_songs_of_all_time.json"
        )
        assert "6i2Qd6OpeRBAzxfscNXeWp " == cls.top_100_playlist.id
        assert "Top 100 Greatest Songs of All Time " == cls.top_100_playlist.name
        assert 118 == len(cls.top_100_playlist.tracks)

        cls.top_100_playlist_statistics = PlaylistStatistics(cls.top_100_playlist.tracks)

        cls.empty_playlist = TestUtils.load_playlist_from_json_file(
            "./test_data/playlist_40389fDt9evjBgcgIMAlxe_empty.json"
        )
        assert "40389fDt9evjBgcgIMAlxe ", cls.empty_playlist.id
        assert "Empty Playlist ", cls.empty_playlist.name
        assert 1, len(cls.empty_playlist.tracks)
        
        cls.empty_playlist_statistics = PlaylistStatistics(cls.empty_playlist.tracks)

    # TODONOW remove those tests later
    def test_top_100_playlist_basic_values(self):
        self.assertEqual("6i2Qd6OpeRBAzxfscNXeWp", self.top_100_playlist.id)
        self.assertEqual("Top 100 Greatest Songs of All Time", self.top_100_playlist.name)
        self.assertEqual(117, len(self.top_100_playlist.tracks))

    def test_empty_playlist_basic_values(self):
        self.assertEqual("40389fDt9evjBgcgIMAlxe", self.empty_playlist.id)
        self.assertEqual("Empty Playlist", self.empty_playlist.name)
        self.assertEqual(0, len(self.empty_playlist.tracks))

    def test_top_100_playlist_total_duration(self):
        self.assertEqual(28022939, self.top_100_playlist_statistics.get_total_duration_ms())

    def test_empty_playlist_total_duration(self):
        self.assertEqual(0, self.empty_playlist_statistics.get_total_duration_ms())

    def test_top_100_playlist_average_duration(self):
        self.assertAlmostEqual(239512, self.top_100_playlist_statistics.get_average_duration_ms(), 0)

    def test_empty_playlist_average_duration(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_duration_ms())

    def test_top_100_playlist_average_popularity(self):
        self.assertAlmostEqual(66, self.top_100_playlist_statistics.get_average_popularity(), 0)

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
        self.assertAlmostEqual(26, self.top_100_playlist_statistics.get_average_acousticness(), 0)

    def test_empty_playlist_average_acousticness(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_acousticness())

    def test_top_100_playlist_average_instrumentalness(self):
        self.assertAlmostEqual(1, self.top_100_playlist_statistics.get_average_instrumentalness(), 0)

    def test_empty_playlist_average_instrumentalness(self):
        self.assertIsNone(self.empty_playlist_statistics.get_average_instrumentalness())

    def test_top_100_playlist_average_valence(self):
        self.assertAlmostEqual(63, self.top_100_playlist_statistics.get_average_valence(), 0)

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
