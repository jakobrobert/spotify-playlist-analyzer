class SpotifyTrack:
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    MODE_STRINGS = ["Minor", "Major"]

    def __init__(self):
        self.id = None
        self.title = None
        self.artist_ids = []
        self.artists = []
        self.duration_ms = 0
        self.release_year = 0
        self.popularity = 0
        self.genres = []
        self.tempo = 0
        self.key = -1
        self.mode = -1
        self.key_signature = None
        self.camelot = None
        self.loudness = 0

    def get_key_string(self):
        return SpotifyTrack.__get_from_list_or_none(SpotifyTrack.KEY_STRINGS, self.key)

    def get_mode_string(self):
        return SpotifyTrack.__get_from_list_or_none(SpotifyTrack.MODE_STRINGS, self.mode)

    @staticmethod
    def __get_from_list_or_none(_list, index):
        if index < 0 or index >= len(_list):
            return None

        return _list[index]
