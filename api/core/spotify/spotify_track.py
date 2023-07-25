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
        self.genres = []
        self.super_genres = []
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

    def update_genres_and_super_genres(self, genres):
        self.genres = genres
        self.__update_super_genres_by_genres(genres)

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

    def __update_super_genres_by_genres(self, genres):
        self.super_genres = []

        for genre in genres:
            super_genre = SpotifyTrack.__get_super_genre_for_genre(genre)
            if super_genre not in self.super_genres:
                self.super_genres.append(super_genre)

    @staticmethod
    def __get_super_genre_for_genre(genre):
        if "pop" in genre:
            return "Pop"

        if "rock" in genre:
            return "Rock"

        if "edm" in genre or "dance" in genre or "house" in genre or "trance" in genre or "hands up" in genre or\
                "hardstyle" in genre or "big room" in genre:
            return "EDM"

        if "hip hop" in genre or "rap" in genre:
            return "Hip Hop / Rap"

        if "schlager" in genre:
            return "Schlager"

        if "black metal" in genre or "death metal" in genre:
            return "Extreme Metal"

        if "metal" in genre:
            return "Metal"

        # TODONOW add other super genres
        return "Others"

    @staticmethod
    def __get_key_signature_from_key_and_mode(key, mode):
        if (key == Key.C and mode == Mode.Major) or (key == Key.A and mode == Mode.Minor):
            return "♮"
        if (key == Key.G and mode == Mode.Major) or (key == Key.E and mode == Mode.Minor):
            return "1♯"
        if (key == Key.D and mode == Mode.Major) or (key == Key.B and mode == Mode.Minor):
            return "2♯"
        if (key == Key.A and mode == Mode.Major) or (key == Key.Fs and mode == Mode.Minor):
            return "3♯"
        if (key == Key.E and mode == Mode.Major) or (key == Key.Cs and mode == Mode.Minor):
            return "4♯"
        if (key == Key.B and mode == Mode.Major) or (key == Key.Gs and mode == Mode.Minor):
            return "5♯"
        if (key == Key.Fs and mode == Mode.Major) or (key == Key.Ds and mode == Mode.Minor):
            return "6♯/6♭"
        if (key == Key.Cs and mode == Mode.Major) or (key == Key.As and mode == Mode.Minor):
            return "5♭"
        if (key == Key.Gs and mode == Mode.Major) or (key == Key.F and mode == Mode.Minor):
            return "4♭"
        if (key == Key.Ds and mode == Mode.Major) or (key == Key.C and mode == Mode.Minor):
            return "3♭"
        if (key == Key.As and mode == Mode.Major) or (key == Key.G and mode == Mode.Minor):
            return "2♭"
        if (key == Key.F and mode == Mode.Major) or (key == Key.D and mode == Mode.Minor):
            return "1♭"

        return "n/a"

    @staticmethod
    def __process_audio_feature_value(value):
        return round(value * 100)
