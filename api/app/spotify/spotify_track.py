class SpotifyTrack:
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    MODE_STRINGS = ["Minor", "Major"]
    KEY_SIGNATURE_STRINGS = ["♮", "1♯", "2♯", "3♯", "4♯", "5♯", "6♯/6♭", "5♭", "4♭", "3♭", "2♭", "1♭"]

    def __init__(self):
        self.id = None
        self.artist_ids = []
        self.artists = []
        self.title = None
        self.duration_ms = 0
        self.release_year = 0
        self.popularity = 0
        self.tempo = 0
        self.key = -1
        self.mode = -1
        self.key_signature = None
        self.camelot = None
        self.loudness = 0
        self.danceability = 0
        self.energy = 0
        self.speechiness = 0
        self.acousticness = 0
        self.instrumentalness = 0
        self.liveness = 0
        self.valence = 0
        self.genres = []

    def get_key_string(self):
        return SpotifyTrack.__get_from_list_or_none(SpotifyTrack.KEY_STRINGS, self.key)

    def get_mode_string(self):
        return SpotifyTrack.__get_from_list_or_none(SpotifyTrack.MODE_STRINGS, self.mode)

    def update_attributes_by_audio_features(self, audio_features):
        self.tempo = audio_features["tempo"]
        self.key = audio_features["key"]
        self.mode = audio_features["mode"]
        key_string = self.get_key_string()
        mode_string = self.get_mode_string()
        self.key_signature = SpotifyTrack.__get_key_signature_from_key_and_mode(key_string, mode_string)
        self.camelot = SpotifyTrack.__get_camelot_from_key_and_mode(key_string, mode_string)
        self.loudness = audio_features["loudness"]
        self.danceability = SpotifyTrack.__process_audio_feature_value(audio_features["danceability"])
        self.energy = SpotifyTrack.__process_audio_feature_value(audio_features["energy"])
        self.speechiness = SpotifyTrack.__process_audio_feature_value(audio_features["speechiness"])
        self.acousticness = SpotifyTrack.__process_audio_feature_value(audio_features["acousticness"])
        self.instrumentalness = SpotifyTrack.__process_audio_feature_value(audio_features["instrumentalness"])
        self.liveness = SpotifyTrack.__process_audio_feature_value(audio_features["liveness"])
        self.valence = SpotifyTrack.__process_audio_feature_value(audio_features["valence"])

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

        return "n/a"

    @staticmethod
    def __get_camelot_from_key_and_mode(key_string, mode_string):
        if key_string == "G♯/A♭" and mode_string == "Minor":
            return "01A"
        if key_string == "B" and mode_string == "Major":
            return "01B"
        if key_string == "D♯/E♭" and mode_string == "Minor":
            return "02A"
        if key_string == "F♯/G♭" and mode_string == "Major":
            return "02B"
        if key_string == "A♯/B♭" and mode_string == "Minor":
            return "03A"
        if key_string == "C♯/D♭" and mode_string == "Major":
            return "03B"
        if key_string == "F" and mode_string == "Minor":
            return "04A"
        if key_string == "G♯/A♭" and mode_string == "Major":
            return "04B"
        if key_string == "C" and mode_string == "Minor":
            return "05A"
        if key_string == "D♯/E♭" and mode_string == "Major":
            return "05B"
        if key_string == "G" and mode_string == "Minor":
            return "06A"
        if key_string == "A♯/B♭" and mode_string == "Major":
            return "06B"
        if key_string == "D" and mode_string == "Minor":
            return "07A"
        if key_string == "F" and mode_string == "Major":
            return "07B"
        if key_string == "A" and mode_string == "Minor":
            return "08A"
        if key_string == "C" and mode_string == "Major":
            return "08B"
        if key_string == "E" and mode_string == "Minor":
            return "09A"
        if key_string == "G" and mode_string == "Major":
            return "09B"
        if key_string == "B" and mode_string == "Minor":
            return "10A"
        if key_string == "D" and mode_string == "Major":
            return "10B"
        if key_string == "F♯/G♭" and mode_string == "Minor":
            return "11A"
        if key_string == "A" and mode_string == "Major":
            return "11B"
        if key_string == "C♯/D♭" and mode_string == "Minor":
            return "12A"
        if key_string == "E" and mode_string == "Major":
            return "12B"

        return "n/a"

    @staticmethod
    def __process_audio_feature_value(value):
        return round(value * 100)

