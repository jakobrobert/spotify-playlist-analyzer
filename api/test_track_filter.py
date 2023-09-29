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
    #   -> might look overkill, especially for numerical attributes because they all use same code,
    #   -> but tests should not make assumptions about the internal structure of the impl.

    @parameterized.expand([
        ["david guetta", True],
        ["David Guetta", True],
        ["   David  Guetta ", True],
        ["dawid guetta", False],
    ])
    def test_filter_by_title(self, title, should_accept):
        filter_params = {
            "filter_by": "title",
            "title_substring": "david guetta"
        }
        track = Track()
        track.title = title
        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [1985, True],
        [1970, False],
        [1990, False]
    ])
    def test_filter_by_release_year(self, release_year, should_accept):
        filter_params = {
            "filter_by": "release_year",
            "min_release_year": 1980,
            "max_release_year": 1989
        }
        track = Track()
        track.release_year = release_year
        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [110, True],
        [90, False],
        [130, False]
    ])
    def test_filter_by_tempo(self, tempo, should_accept):
        filter_params = {
            "filter_by": "tempo",
            "min_tempo": 100,
            "max_tempo": 120
        }
        track = Track()
        track.tempo = tempo
        self.__test_filter_tracks(filter_params, should_accept, track)

    def __test_filter_tracks(self, filter_params, should_accept, track):
        expected_filtered_tracks_length = 1 if should_accept else 0

        track_filter = TrackFilter([track], filter_params)
        actual_filtered_tracks_length = len(track_filter.filter_tracks())

        self.assertEqual(expected_filtered_tracks_length, actual_filtered_tracks_length)
