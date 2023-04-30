class SpotifyTrack:
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    MODE_STRINGS = ["Minor", "Major"]
    KEY_SIGNATURE_STRINGS = ["♮", "1♯", "2♯", "3♯", "4♯", "5♯", "6♯/6♭", "5♭", "4♭", "3♭", "2♭", "1♭"]

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

    def update_key_signature(self):
        self.key_signature = SpotifyTrack.__get_key_signature_from_key_and_mode(
            self.get_key_string(), self.get_mode_string())

    @staticmethod
    def __get_from_list_or_none(_list, index):
        if index < 0 or index >= len(_list):
            return None

        return _list[index]

    @staticmethod
    def __get_key_signature_from_key_and_mode(key_string, mode_string):
        if (key_string == "C" and mode_string == "Major") or (key_string == "A" and mode_string == "Minor"):
            return "♮"
        if (key_string == "G" and mode_string == "Major") or (key_string == "E" and mode_string == "Minor"):
            return "1♯"
        if (key_string == "D" and mode_string == "Major") or (key_string == "B" and mode_string == "Minor"):
            return "2♯"
        if (key_string == "A" and mode_string == "Major") or (key_string == "F♯/G♭" and mode_string == "Minor"):
            return "3♯"
        if (key_string == "E" and mode_string == "Major") or (key_string == "C♯/D♭" and mode_string == "Minor"):
            return "4♯"
        if (key_string == "B" and mode_string == "Major") or (key_string == "G♯/A♭" and mode_string == "Minor"):
            return "5♯"
        if (key_string == "F♯/G♭" and mode_string == "Major") or (key_string == "D♯/E♭" and mode_string == "Minor"):
            return "6♯/6♭"
        if (key_string == "C♯/D♭" and mode_string == "Major") or (key_string == "A♯/B♭" and mode_string == "Minor"):
            return "5♭"
        if (key_string == "G♯/A♭" and mode_string == "Major") or (key_string == "F" and mode_string == "Minor"):
            return "4♭"
        if (key_string == "D♯/E♭" and mode_string == "Major") or (key_string == "C" and mode_string == "Minor"):
            return "3♭"
        if (key_string == "A♯/B♭" and mode_string == "Major") or (key_string == "G" and mode_string == "Minor"):
            return "2♭"
        if (key_string == "F" and mode_string == "Major") or (key_string == "D" and mode_string == "Minor"):
            return "1♭"
