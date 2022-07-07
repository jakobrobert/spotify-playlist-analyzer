class SpotifyTrack:
    KEY_NAMES = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]

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
