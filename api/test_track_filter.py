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
        ["MaxMustermann42", True],
        ["MaxMuster", True],
        ["maxmuster", True],
        ["  max muster  ", True],
        ["maymuster", False],
    ])
    def test_filter_by_added_by(self, added_by_substring, should_accept):
        filter_params = {
            "filter_by": "added_by",
            "added_by_substring": added_by_substring
        }
        track = Track()
        track.added_by = "MaxMustermann42"

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        ["dance pop", True],
        ["soft rock", True],
        ["pop", True],
        ["rock", True],
        ["  dance   pop  ", True],
        ["  soft   rock  ", True],
        ["pop rock", False],
        ["german dance", False],
    ])
    def test_filter_by_genres(self, genres_substring, should_accept):
        filter_params = {
            "filter_by": "genres",
            "genres_substring": genres_substring
        }
        track = Track()
        track.genres = ["dance pop", "soft rock"]

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        ["Pop", True],
        ["Classical", True],
        ["Classic", True],
        ["pop", True],
        ["classical", True],
        ["  pop  ", True],
        ["  classical  ", True],
        ["Rock", False],
        ["Klassik", False],
    ])
    def test_filter_by_super_genres(self, super_genres_substring, should_accept):
        filter_params = {
            "filter_by": "super_genres",
            "super_genres_substring": super_genres_substring
        }
        track = Track()
        track.super_genres = ["Pop", "Classical"]

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [4, True],
        [6, False]
    ])
    def test_filter_by_key(self, expected_key, should_accept):
        filter_params = {
            "filter_by": "key",
            "expected_key": expected_key
        }
        track = Track()
        track.key = 4

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [1, True],
        [0, False]
    ])
    def test_filter_by_mode(self, expected_mode, should_accept):
        filter_params = {
            "filter_by": "mode",
            "expected_mode": expected_mode
        }
        track = Track()
        track.mode = 1

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [16, True],
        [4, False]
    ])
    def test_filter_by_key_and_mode_pair(self, expected_key_and_mode_pair, should_accept):
        filter_params = {
            "filter_by": "key_and_mode_pair",
            "expected_key_and_mode_pair": expected_key_and_mode_pair
        }
        track = Track()
        track.key_and_mode_pair = 16

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        ["4♯", True],
        ["5♭", False]
    ])
    def test_filter_by_key_signature(self, expected_key_signature, should_accept):
        filter_params = {
            "filter_by": "key_signature",
            "expected_key_signature": expected_key_signature
        }
        track = Track()
        track.key_signature = "4♯"

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
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_popularity(self, min_popularity, max_popularity, should_accept):
        filter_params = {
            "filter_by": "popularity",
            "min_popularity": min_popularity,
            "max_popularity": max_popularity
        }
        track = Track()
        track.popularity = 55

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

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_loudness(self, min_loudness, max_loudness, should_accept):
        filter_params = {
            "filter_by": "loudness",
            "min_loudness": min_loudness,
            "max_loudness": max_loudness
        }
        track = Track()
        track.loudness = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_danceability(self, min_danceability, max_danceability, should_accept):
        filter_params = {
            "filter_by": "danceability",
            "min_danceability": min_danceability,
            "max_danceability": max_danceability
        }
        track = Track()
        track.danceability = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_energy(self, min_energy, max_energy, should_accept):
        filter_params = {
            "filter_by": "energy",
            "min_energy": min_energy,
            "max_energy": max_energy
        }
        track = Track()
        track.energy = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_valence(self, min_valence, max_valence, should_accept):
        filter_params = {
            "filter_by": "valence",
            "min_valence": min_valence,
            "max_valence": max_valence
        }
        track = Track()
        track.valence = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_instrumentalness(self, min_instrumentalness, max_instrumentalness, should_accept):
        filter_params = {
            "filter_by": "instrumentalness",
            "min_instrumentalness": min_instrumentalness,
            "max_instrumentalness": max_instrumentalness
        }
        track = Track()
        track.instrumentalness = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_acousticness(self, min_acousticness, max_acousticness, should_accept):
        filter_params = {
            "filter_by": "acousticness",
            "min_acousticness": min_acousticness,
            "max_acousticness": max_acousticness
        }
        track = Track()
        track.acousticness = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_liveness(self, min_liveness, max_liveness, should_accept):
        filter_params = {
            "filter_by": "liveness",
            "min_liveness": min_liveness,
            "max_liveness": max_liveness
        }
        track = Track()
        track.liveness = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    @parameterized.expand([
        [50, 60, True],
        [55, 60, True],
        [56, 60, False],
        [50, 55, True],
        [50, 54, False]
    ])
    def test_filter_by_speechiness(self, min_speechiness, max_speechiness, should_accept):
        filter_params = {
            "filter_by": "speechiness",
            "min_speechiness": min_speechiness,
            "max_speechiness": max_speechiness
        }
        track = Track()
        track.speechiness = 55

        self.__test_filter_tracks(filter_params, should_accept, track)

    def __test_filter_tracks(self, filter_params, should_accept, track):
        expected_filtered_tracks_length = 1 if should_accept else 0
        track_filter = TrackFilter([track], filter_params)

        actual_filtered_tracks_length = len(track_filter.filter_tracks())

        self.assertEqual(expected_filtered_tracks_length, actual_filtered_tracks_length)
