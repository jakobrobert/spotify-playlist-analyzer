class SpotifyTrack:
    def __init__(self):
        self.title = "n/a"
        self.artists = []
        self.duration_ms = 0
        self.year_of_release = -1
        self.genres = []
        self.tempo = -1.0
        self.key = "n/a"
        self.mode = "n/a"
        self.camelot = "n/a"
        self.loudness = -1.0

    def get_duration_string(self):
        total_seconds = self.duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
