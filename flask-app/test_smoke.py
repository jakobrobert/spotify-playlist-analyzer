import configparser
import unittest

from spotify_playlist_analyzer import app

config = configparser.ConfigParser()
config.read("config.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]


class TestSmoke(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        url = f"{URL_PREFIX}"
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_choose_one_playlist(self):
        url = f"{URL_PREFIX}choose-one-playlist"
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # TODONOW uncomment
    """
    def test_playlist(self):
        url = f"{URL_PREFIX}playlist/1v1enByYGutAxxH06UW3cf"
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    """