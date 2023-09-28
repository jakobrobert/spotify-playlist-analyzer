import unittest

from core.playlist.track import Track
from core.track_filter import TrackFilter


class TestTrackFilter(unittest.TestCase):
    def test_filter_tempo(self):
        filter_params = {
            "filter_by": "tempo",
            "min_tempo": 100,
            "max_tempo": 120
        }
        accepted_track = Track()
        accepted_track.tempo = 110
        not_accepted_track_1 = Track()
        not_accepted_track_1.tempo = 90
        not_accepted_track_2 = Track()
        not_accepted_track_2.tempo = 130
        tracks = [accepted_track, not_accepted_track_1, not_accepted_track_2]
        expected_filtered_tracks = [accepted_track]

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks = track_filter.filter_tracks()

        self.assertEqual(expected_filtered_tracks, actual_filtered_tracks)
