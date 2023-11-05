import unittest

from parameterized import parameterized

from core.views.view_utils import ViewUtils
from spotify_playlist_analyzer import app


class TestSmoke(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    @parameterized.expand([
        ["https://open.spotify.com/playlist/4PEUZYZ3RoKEcZQoGqu5mV?si=0c08f72180474249", "4PEUZYZ3RoKEcZQoGqu5mV"],
        ["https://open.spotify.com/playlist/4PEUZYZ3RoKEcZQoGqu5mV", "4PEUZYZ3RoKEcZQoGqu5mV"],
    ])
    def test_get_playlist_id_from_playlist_url_valid(self, playlist_url, expected_playlist_id):
        actual_playlist_id = ViewUtils.get_playlist_id_from_playlist_url(playlist_url)
        self.assertEqual(expected_playlist_id, actual_playlist_id)

    @parameterized.expand([
        ["foo"],
        ["https://open.spotify.com/intl-de/track/5XcZRgJv3zMhTqCyESjQrF?si=0815a93806cd484b"],
    ])
    def test_get_playlist_id_from_playlist_url_invalid(self, playlist_url):
        with self.assertRaises(Exception):
            ViewUtils.get_playlist_id_from_playlist_url(playlist_url)

    @parameterized.expand([
        ["https://open.spotify.com/intl-de/track/5XcZRgJv3zMhTqCyESjQrF?si=0815a93806cd484b", "5XcZRgJv3zMhTqCyESjQrF"],
        ["https://open.spotify.com/intl-de/track/5XcZRgJv3zMhTqCyESjQrF", "5XcZRgJv3zMhTqCyESjQrF"],
    ])
    def test_get_track_id_from_track_url_valid(self, track_url, expected_track_id):
        actual_track_id = ViewUtils.get_track_id_from_track_url(track_url)
        self.assertEqual(expected_track_id, actual_track_id)

    @parameterized.expand([
        ["foo"],
        ["https://open.spotify.com/playlist/4PEUZYZ3RoKEcZQoGqu5mV?si=0c08f72180474249"],
    ])
    def test_get_track_id_from_track_url_invalid(self, track_url):
        with self.assertRaises(Exception):
            ViewUtils.get_track_id_from_track_url(track_url)
