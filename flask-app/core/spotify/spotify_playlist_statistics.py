from core.spotify.spotify_track import SpotifyTrack


class SpotifyPlaylistStatistics:
    def __init__(self):
        self.total_duration_ms = 0.0
        self.average_duration_ms = 0.0
        self.average_release_year = 0.0
        self.average_popularity = 0.0
        self.average_tempo = 0.0

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

        # TODONOW move into utils
        return SpotifyTrack.get_duration_string_helper(self.average_duration_ms)

    def get_average_release_year_string(self):
        if not self.average_release_year:
            return "n/a"

        return f"{self.average_release_year:.1f}"

    def get_average_popularity_string(self):
        if not self.average_popularity:
            return "n/a"

        return f"{self.average_popularity:.1f}"

    def get_average_tempo_string(self):
        if not self.average_tempo:
            return "n/a"

        return f"{self.average_tempo:.1f}"