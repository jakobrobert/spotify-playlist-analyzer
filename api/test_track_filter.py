import unittest

from core.playlist.track import Track
from core.track_filter import TrackFilter


class TestTrackFilter(unittest.TestCase):
    # TODONOW refactor duplicated code
    def test_filter_by_tempo_accepted(self):
        filter_params = {
            "filter_by": "tempo",
            "min_tempo": 100,
            "max_tempo": 120
        }

        accepted_track = Track()
        accepted_track.tempo = 110
        tracks = [accepted_track]
        expected_filtered_tracks = [accepted_track]

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks = track_filter.filter_tracks()

        self.assertEqual(expected_filtered_tracks, actual_filtered_tracks)

    def test_filter_by_tempo_not_accepted_because_too_small(self):
        filter_params = {
            "filter_by": "tempo",
            "min_tempo": 100,
            "max_tempo": 120
        }

        accepted_track = Track()
        accepted_track.tempo = 90
        tracks = [accepted_track]

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks = track_filter.filter_tracks()
        expected_filtered_tracks = []

        self.assertEqual(expected_filtered_tracks, actual_filtered_tracks)

    def test_filter_by_tempo_not_accepted_because_too_big(self):
        filter_params = {
            "filter_by": "tempo",
            "min_tempo": 100,
            "max_tempo": 120
        }

        accepted_track = Track()
        accepted_track.tempo = 130
        tracks = [accepted_track]

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks = track_filter.filter_tracks()
        expected_filtered_tracks = []

        self.assertEqual(expected_filtered_tracks, actual_filtered_tracks)
