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
        accepted_track.id = "accepted"
        accepted_track.tempo = 110
        not_accepted_track_1 = Track()
        not_accepted_track_1.id = "not accepted 1"
        not_accepted_track_1.tempo = 90
        not_accepted_track_2 = Track()
        not_accepted_track_2.id = "not accepted 2"
        not_accepted_track_2.tempo = 130
        tracks = [accepted_track, not_accepted_track_1, not_accepted_track_2]
        expected_filtered_track_ids = ["accepted", "not accepted 1"] # TODONOW fix, error on purpose

        track_filter = TrackFilter(tracks, filter_params)
        actual_filtered_tracks = track_filter.filter_tracks()
        actual_filtered_track_ids = [track.id for track in actual_filtered_tracks]

        self.assertEqual(expected_filtered_track_ids, actual_filtered_track_ids)
