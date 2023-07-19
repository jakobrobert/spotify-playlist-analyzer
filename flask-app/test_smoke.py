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
        playlist_id = "1v1enByYGutAxxH06UW3cf"
        self.__test_get_request(f"playlist/{playlist_id}")

    def test_compare_playlists(self):
        playlist_id_1 = "1v1enByYGutAxxH06UW3cf"
        playlist_id_2 = "37i9dQZF1DXcBWIGoYBM5M"
        params = {"playlist_id_1": playlist_id_1, "playlist_id_2": playlist_id_2}
        self.__test_get_request(f"compare-playlists", params)

    # TODONOW fails as expected due to bug #238
    def test_track(self):
        track_id = "4cOdK2wGLETKBW3PvgPWqT"
        self.__test_get_request(f"track/{track_id}")

    def test_search_tracks(self):
        query = "Avicii"
        params = {"query": query}
        self.__test_get_request("search-tracks", params)

    # TODONOW add several tests for playlist sort tracks, one for each attribute
    #   -> But for each attribute, ONLY ascending is enough. For now, only smoke tests, no detailed functional tests

    # TODONOW add several tests for playlist filter tracks, one for each attribute
    #   -> But for each attribute, ONLY one value / range. For now, only smoke tests, no detailed functional tests

    # TODONOW add several tests for get_attribute_distribution_of_playlist, one for each attribute
    #   -> should be able to reproduce bug #236 for attributes key & mode.

    # TODONOW add several tests compare_attribute_distribution_of_playlists, one for each attribute
    #   -> should be able to reproduce bug #236 for attributes key & mode.

    # TODOLATER Did NOT add test for route export_playlist on purpose.
    #   -> is rather complicated, need to send track ids by post request, needs to have a valid access token
    #   -> might add later, but then not in smoke tests, would be a more detailed functional test

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