import unittest

from parameterized import parameterized

from core.playlist.track import Track
from core.track_filter import TrackFilter


class TestTrackFilter(unittest.TestCase):
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
        tracks = [track]
        expected_filtered_tracks_length = 1 if should_accept else 0

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks_length = len(track_filter.filter_tracks())

        self.assertEqual(expected_filtered_tracks_length, actual_filtered_tracks_length)

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
        tracks = [track]
        expected_filtered_tracks_length = 1 if should_accept else 0

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks_length = len(track_filter.filter_tracks())

        self.assertEqual(expected_filtered_tracks_length, actual_filtered_tracks_length)
