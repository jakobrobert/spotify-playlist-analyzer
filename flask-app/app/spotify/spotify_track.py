class SpotifyTrack:
    def __init__(self):
        self.id = "n/a"
        self.title = "n/a"
        self.artist_ids = []
        self.artists = []
        self.duration_ms = 0
        self.release_year = 0
        self.genres = []
        self.tempo = 0
        self.key = -1
        self.mode = -1
        self.camelot = "n/a"
        self.loudness = 0

    def get_artists_string(self):
        return ", ".join(self.artists)

    def get_duration_string(self):
        return self.get_duration_string_helper(self.duration_ms)

    def get_genres_string(self):
        return ", ".join(self.genres)

    def get_tempo_string(self):
        return f"{self.tempo:.1f}"

    def get_loudness_string(self):
        return f"{self.loudness:.1f}"

    @staticmethod
    def get_duration_string_helper(duration_ms):
        total_seconds = duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
