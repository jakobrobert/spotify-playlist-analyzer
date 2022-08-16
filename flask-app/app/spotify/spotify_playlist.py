# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.total_duration_ms = 0.0
        self.average_duration_ms = 0.0
        self.average_release_year = 0.0
        self.average_popularity = 0.0
        self.average_tempo = 0.0
        self.tracks = []

    # Cannot be static, else template code cannot access it
    def percentage_to_string(self, percentage):
        return f"{percentage:.1f}"

    def get_total_duration_string(self):
        total_seconds = self.total_duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60

        return f"{total_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"

    def get_average_duration_string(self):
        return SpotifyTrack.get_duration_string_helper(int(self.average_duration_ms))

    def get_average_release_year_string(self):
        return f"{self.average_release_year:.1f}"

    def get_average_popularity_string(self):
        return f"{self.average_popularity:.1f}"

    def get_average_tempo_string(self):
        return f"{self.average_tempo:.1f}"
