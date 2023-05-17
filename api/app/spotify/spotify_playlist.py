import json

# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack
from playlist_statistics.playlist_statistics import PlaylistStatistics


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []
        self.statistics = None

    # TODO Inline all delegating methods & get rid of update_statistics method.
    #  -> Create PlaylistStatistics object outside, based on playlist, once playlist is processed.
    def get_total_duration_ms(self):
        self.update_statistics()
        return self.statistics.get_total_duration_ms()

    def get_average_duration_ms(self):
        self.update_statistics()
        return self.statistics.get_average_duration_ms()

    def get_average_popularity(self):
        self.update_statistics()
        return self.statistics.get_average_popularity()

    def get_average_release_year(self):
        self.update_statistics()
        return self.statistics.get_average_release_year()

    def get_average_tempo(self):
        self.update_statistics()
        return self.statistics.get_average_tempo()

    # TODO this is temporarily called for each method where statistics needed
    #   Will move it out later, when methods are inlined and statistics accessed directly from outside
    def update_statistics(self):
        self.statistics = PlaylistStatistics(self.tracks)

    def get_duration_interval_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_duration_interval_to_percentage()

    def get_release_year_interval_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_release_year_interval_to_percentage()

    def get_popularity_interval_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_popularity_interval_to_percentage()

    def get_tempo_interval_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_tempo_interval_to_percentage()

    def get_key_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_key_to_percentage()

    def get_mode_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_mode_to_percentage()
    
    def get_key_signature_to_percentage(self):
        self.update_statistics()
        return self.statistics.get_key_signature_to_percentage()

    # TODO can remove
    @staticmethod
    def __get_duration_string(duration_ms):
        total_seconds = duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
