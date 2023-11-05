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
