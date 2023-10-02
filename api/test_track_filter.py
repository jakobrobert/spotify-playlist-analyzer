import unittest

from parameterized import parameterized

from core.playlist.track import Track
from core.track_filter import TrackFilter


class TestTrackFilter(unittest.TestCase):
    def test_filter_by_invalid(self):
        filter_params = {
            "filter_by": "foobar"
        }
        track = Track()
        track_filter = TrackFilter([track], filter_params)

        with self.assertRaises(Exception):
            track_filter.filter_tracks()

    # TODONOW add tests for all attributes, see TrackFilter
    #   -> might look like overkill, especially for numerical attributes because they all use same code,
    #   -> but tests should not make assumptions about the internal structure of the impl.

    @parameterized.expand([
        ["Avicii", True],
        ["David Guetta", True],
        ["Avic", True],
        ["avicii", True],
        ["  avicii  ", True],
        ["  david   guetta  ", True],
        ["aviciii", False],
        ["Dawid", False],
    ])
    def test_filter_by_artists(self, artists_substring, should_accept):
        filter_params = {
            "filter_by": "artists",
            "artists_substring": artists_substring
        }
        track = Track()
        track.artists = ["Avicii", "David Guetta"]

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        ["Wake Me Up", True],
        ["Wake Me", True],
        ["wake me", True],
        ["  wake   me  ", True],
        ["waje Me", False],
    ])
    def test_filter_by_title(self, title_substring, should_accept):
        filter_params = {
            "filter_by": "title",
            "title_substring": title_substring
        }
        track = Track()
        track.title = "Wake Me Up"

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [1980, 1989, True],
        [1985, 1989, True],
        [1986, 1989, False],
        [1980, 1985, True],
        [1980, 1984, False]
    ])
    def test_filter_by_release_year(self, min_release_year, max_release_year, should_accept):
        filter_params = {
            "filter_by": "release_year",
            "min_release_year": min_release_year,
            "max_release_year": max_release_year
        }
        track = Track()
        track.release_year = 1985

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [100, 110, True],
        [105, 110, True],
        [106, 110, False],
        [100, 105, True],
        [100, 104, False]
    ])
    def test_filter_by_tempo(self, min_tempo, max_tempo, should_accept):
        filter_params = {
            "filter_by": "tempo",
            "min_tempo": min_tempo,
            "max_tempo": max_tempo
        }
        track = Track()
        track.tempo = 105

        self.__test_filter_tracks(filter_params, should_accept, track)

    def __test_filter_tracks(self, filter_params, should_accept, track):
        expected_filtered_tracks_length = 1 if should_accept else 0
        track_filter = TrackFilter([track], filter_params)

        actual_filtered_tracks_length = len(track_filter.filter_tracks())

        self.assertEqual(expected_filtered_tracks_length, actual_filtered_tracks_length)
