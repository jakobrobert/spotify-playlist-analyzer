import unittest

from core.spotify.spotify_track import SpotifyTrack


class TestSuperGenre(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pop(self):
        # TODONOW refactor: Extract util method so do not need to create track
        track = SpotifyTrack()
        genres = ["dance pop"]
        track.update_genres_and_super_genres(genres)
        expected = ["Pop"]
        self.assertEqual(expected, track.super_genres)

    def test_edm(self):
        # TODONOW refactor: Extract util method so do not need to create track
        track = SpotifyTrack()
        genres = ["hip house"]
        track.update_genres_and_super_genres(genres)
        expected = ["EDM"]
        self.assertEqual(expected, track.super_genres)
