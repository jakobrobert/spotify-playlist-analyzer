import configparser
import unittest

from spotify_playlist_analyzer import app

# TODONOW move into setUp?
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
        self.__test_get_request(url)

    def test_choose_one_playlist(self):
        url = f"{URL_PREFIX}choose-one-playlist"
        self.__test_get_request(url)

    def test_choose_one_playlist(self):
        url = f"{URL_PREFIX}choose-one-playlist"
        self.__test_get_request(url)

    def test_choose_playlists_for_comparison(self):
        url = f"{URL_PREFIX}choose-playlists-for-comparison"
        self.__test_get_request(url)

    def test_choose_one_track(self):
        url = f"{URL_PREFIX}choose-one-track"
        self.__test_get_request(url)

    def test_enter_query_to_search_tracks(self):
        url = f"{URL_PREFIX}enter-query-to-search-tracks"
        self.__test_get_request(url)

    def test_playlist(self):
        url = f"{URL_PREFIX}playlist/1v1enByYGutAxxH06UW3cf"
        self.__test_get_request(url)

    def __test_get_request(self, url):
        # TODONOW also move usage of URL_PREFIX into __test_get_request to reduce duplication
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
