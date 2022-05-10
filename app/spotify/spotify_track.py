class SpotifyTrack:
    KEY_NAMES = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]

    def __init__(self):
        self.title = "n/a"
        self.artists = []
        self.duration_ms = 0
        self.year_of_release = 0
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

    def get_key_string(self):
        if self.key < 0 or self.key >= len(SpotifyTrack.KEY_NAMES):
            return "n/a"

        return SpotifyTrack.KEY_NAMES[self.key]

    def get_mode_string(self):
        if self.mode == 0:
            return "Minor"

        if self.mode == 1:
            return "Major"

        return "n/a"

    def get_loudness_string(self):
        return f"{self.loudness:.1f}"

    @staticmethod
    def get_duration_string_helper(duration_ms):
        total_seconds = duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
