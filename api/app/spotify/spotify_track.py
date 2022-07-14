class SpotifyTrack:
    MODE_STRINGS = ["Minor", "Major"]
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]

    def __init__(self):
        self.id = None
        self.title = None
        self.artist_ids = []
        self.artists = []
        self.duration_ms = 0
        self.release_year = 0
        self.genres = []
        self.tempo = 0
        self.key = -1
        self.mode = -1
        self.key_signature = None
        self.camelot = None
        self.loudness = 0

    def get_key_string(self):
        if self.key < 0 or self.key >= len(SpotifyTrack.KEY_STRINGS):
            return None

        return SpotifyTrack.KEY_STRINGS[self.key]

    def get_mode_string(self):
        # TODO duplicated code with get_key_string, extract __get_from_list_or_None
        if self.mode < 0 or self.mode >= len(SpotifyTrack.MODE_STRINGS):
            return None

        return SpotifyTrack.MODE_STRINGS[self.mode]
