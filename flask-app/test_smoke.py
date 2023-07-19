import configparser
import unittest

from spotify_playlist_analyzer import app


class TestSmoke(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

        config = configparser.ConfigParser()
        config.read("config.ini")
        self.base_url = config["DEFAULT"]["URL_PREFIX"]

    def tearDown(self):
        pass

    def test_index(self):
        self.__test_get_request("")

    def test_choose_one_playlist(self):
        self.__test_get_request("choose-one-playlist")

    def test_choose_playlists_for_comparison(self):
        self.__test_get_request("choose-playlists-for-comparison")

    def test_choose_one_track(self):
        self.__test_get_request("choose-one-track")

    def test_enter_query_to_search_tracks(self):
        self.__test_get_request("enter-query-to-search-tracks")

    def test_playlist(self):
        self.__test_get_request("playlist/1v1enByYGutAxxH06UW3cf")

    def __test_get_request(self, sub_url):
        # TODONOW also move usage of URL_PREFIX into __test_get_request to reduce duplication
        url = f"{self.base_url}{sub_url}"
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
