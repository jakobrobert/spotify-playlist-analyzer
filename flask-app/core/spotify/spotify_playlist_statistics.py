from core.spotify.spotify_track import SpotifyTrack


class SpotifyPlaylistStatistics:
    def __init__(self):
        self.total_duration_ms = 0
        self.average_duration_ms = 0
        self.average_release_year = 0
        self.average_popularity = 0
        self.average_tempo = 0
        self.average_danceability = 0
        self.average_energy = 0
        self.average_valence = 0
        self.average_instrumentalness = 0
        self.average_acousticness = 0
        self.average_liveness = 0
        self.average_speechiness = 0

    def get_total_duration_string(self):
        total_seconds = self.total_duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60

        return f"{total_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"

    def get_average_duration_string(self):
        if not self.average_duration_ms:
            return "n/a"

        # TODOLATER move into utils
        return SpotifyTrack.get_duration_string_helper(self.average_duration_ms)

    def get_average_release_year_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_release_year)

    def get_average_popularity_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_popularity)

    def get_average_tempo_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_tempo)

    # TODONOW implement new methods get_average_x_string
    def get_average_danceability_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_danceability)

    def get_average_energy_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_energy)

    def get_average_valence_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_valence)

    def get_average_instrumentalness_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_instrumentalness)

    def get_average_acousticness_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_acousticness)

    def get_average_liveness_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_liveness)

    def get_average_speechiness_string(self):
        return SpotifyPlaylistStatistics.number_to_string(self.average_speechiness)

    @staticmethod
    def number_to_string(value):
        if not value:
            return "n/a"

        return f"{value:.1f}"
