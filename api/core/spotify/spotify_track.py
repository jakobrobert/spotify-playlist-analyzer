class SpotifyTrack:
    class Key:
        C = 0
        Cs = Db = 1
        D = 2
        Ds = Eb = 3
        E = 4
        F = 5
        Fs = Gb = 6
        G = 7
        Gs = Ab = 8
        A = 9
        As = Bb = 10
        B = 11

    class Mode:
        Minor = 0
        Major = 1

    # TODONOW those two are still needed for endpoints valid-keys, valid-modes. Should remove those endpoints?
    #   Now the App already knows those strings.
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
        self.genres = []

        # Audio Features
        self.tempo = 0
        self.key = -1
        self.mode = -1
        self.key_signature = None
        self.loudness = 0
        self.danceability = 0
        self.energy = 0
        self.valence = 0
        self.instrumentalness = 0
        self.acousticness = 0
        self.liveness = 0
        self.speechiness = 0

    def update_attributes_by_audio_features(self, audio_features):
        self.tempo = audio_features["tempo"]
        self.key = audio_features["key"]
        self.mode = audio_features["mode"]
        self.key_signature = SpotifyTrack.__get_key_signature_from_key_and_mode(self.key, self.mode)
        self.loudness = audio_features["loudness"]
        self.danceability = SpotifyTrack.__process_audio_feature_value(audio_features["danceability"])
        self.energy = SpotifyTrack.__process_audio_feature_value(audio_features["energy"])
        self.valence = SpotifyTrack.__process_audio_feature_value(audio_features["valence"])
        self.instrumentalness = SpotifyTrack.__process_audio_feature_value(audio_features["instrumentalness"])
        self.acousticness = SpotifyTrack.__process_audio_feature_value(audio_features["acousticness"])
        self.liveness = SpotifyTrack.__process_audio_feature_value(audio_features["liveness"])
        self.speechiness = SpotifyTrack.__process_audio_feature_value(audio_features["speechiness"])

    @staticmethod
    def __get_from_list_or_none(_list, index):
        if index < 0 or index >= len(_list):
            return None

        return _list[index]

    @staticmethod
    def __get_key_signature_from_key_and_mode(key, mode):
        print(f"key: {key}, key == C: {(key == SpotifyTrack.Key.C)}")
        print(f"mode: {mode}, mode == Minor: {(mode == SpotifyTrack.Mode.Minor)}")

        if (key == SpotifyTrack.Key.C and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.A and mode == SpotifyTrack.Mode.Minor):
            return "♮"
        if (key == SpotifyTrack.Key.G and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.E and mode == SpotifyTrack.Mode.Minor):
            return "1♯"
        if (key == SpotifyTrack.Key.D and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.B and mode == SpotifyTrack.Mode.Minor):
            return "2♯"
        if (key == SpotifyTrack.Key.A and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.Fs and mode == SpotifyTrack.Mode.Minor):
            return "3♯"
        if (key == SpotifyTrack.Key.E and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.Cs and mode == SpotifyTrack.Mode.Minor):
            return "4♯"
        if (key == SpotifyTrack.Key.B and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.Gs and mode == SpotifyTrack.Mode.Minor):
            return "5♯"
        if (key == SpotifyTrack.Key.Fs and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.Ds and mode == SpotifyTrack.Mode.Minor):
            return "6♯/6♭"
        if (key == SpotifyTrack.Key.Cs and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.As and mode == SpotifyTrack.Mode.Minor):
            return "5♭"
        if (key == SpotifyTrack.Key.Gs and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.F and mode == SpotifyTrack.Mode.Minor):
            return "4♭"
        if (key == SpotifyTrack.Key.Ds and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.C and mode == SpotifyTrack.Mode.Minor):
            return "3♭"
        if (key == SpotifyTrack.Key.As and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.G and mode == SpotifyTrack.Mode.Minor):
            return "2♭"
        if (key == SpotifyTrack.Key.F and mode == SpotifyTrack.Mode.Major) or (key == SpotifyTrack.Key.D and mode == SpotifyTrack.Mode.Minor):
            return "1♭"

        return "n/a"

    @staticmethod
    def __process_audio_feature_value(value):
        return round(value * 100)
