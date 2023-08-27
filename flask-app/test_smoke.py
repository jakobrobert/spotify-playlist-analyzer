import configparser
import unittest
from urllib.parse import urlencode

from spotify_playlist_analyzer import app

PLAYLIST_ID_1 = "1v1enByYGutAxxH06UW3cf"
PLAYLIST_ID_2 = "5CgE5f0xzNTTHd6zlYRyzW"
PLAYLIST_ID_EMPTY = "5HYNylDNFV1bU6WrF1ot5Y"
TRACK_ID = "4cOdK2wGLETKBW3PvgPWqT"


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
        self.__test_get_request(f"playlist/{PLAYLIST_ID_1}")

    def test_playlist_empty(self):
        self.__test_get_request(f"playlist/{PLAYLIST_ID_EMPTY}")

    # Only testing one attribute because else would take too long and also too many requests to Spotify API
    # For Smoke test this is sufficient, only broad test that basic functionality works
    # For detailed functionality tests, would need proper unit tests and avoid requests to Spotify API
    def test_playlist_sort_tracks(self):
        params = {"sort_by": "release_year", "order": "ascending"}
        self.__test_get_request(f"playlist/{PLAYLIST_ID_1}", params)

    def test_playlist_filter_tracks(self):
        params = {"filter_by": "release_year", "min_release_year": "1980", "max_release_year": "1989"}
        self.__test_get_request(f"playlist/{PLAYLIST_ID_1}", params)

    def test_compare_playlists(self):
        params = {"playlist_id_1": PLAYLIST_ID_1, "playlist_id_2": PLAYLIST_ID_2}
        self.__test_get_request(f"compare-playlists", params)

    def test_track(self):
        self.__test_get_request(f"track/{TRACK_ID}")

    def test_search_tracks(self):
        query = "Avicii"
        params = {"query": query}
        self.__test_get_request("search-tracks", params)

    def test_attribute_distribution(self):
        params = {"attribute": "release_year"}
        self.__test_get_request(f"playlist/{PLAYLIST_ID_1}/attribute-distribution", params)

    def test_compare_attribute_distribution(self):
        params = {"playlist_id_1": PLAYLIST_ID_1, "playlist_id_2": PLAYLIST_ID_2, "attribute": "release_year"}
        self.__test_get_request(f"compare-attribute-distribution-of-playlists", params)

    # NOTE: Did NOT add test for endpoint export_playlist on purpose.
    # -> is rather complicated, need to send track ids by post request, needs to have a valid access token
    # -> might add later, but then not in smoke tests, would be a more detailed functional test

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
