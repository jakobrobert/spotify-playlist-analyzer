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
        response = self.app.get(f"{URL_PREFIX}/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
