import configparser
import unittest
from urllib.parse import urlencode

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

    def test_compare_playlists(self):
        params = {
            "playlist_id_1": "1v1enByYGutAxxH06UW3cf",
            "playlist_id_2": "37i9dQZF1DXcBWIGoYBM5M"
        }
        self.__test_get_request(f"compare-playlists", params)

    # TODONOW fails as expected due to bug #238
    def test_track(self):
        self.__test_get_request("track/4cOdK2wGLETKBW3PvgPWqT")

    def test_search_tracks(self):
        params = {"query": "Avicii"}
        self.__test_get_request("search-tracks", params)

    def __test_get_request(self, sub_url, params=None):
        encoded_query_params = TestSmoke.__encode_query_params(params)
        url = f"{self.base_url}{sub_url}{encoded_query_params}"
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def __encode_query_params(query_params):
        if not query_params:
            return ""

        return f"?{urlencode(query_params)}"