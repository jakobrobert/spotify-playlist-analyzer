class Keys:
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


class Modes:
    Minor = 0
    Major = 1


class SuperGenres:
    Pop = "Pop"
    Rock = "Rock"
    EDM = "EDM"
    HipHopOrRap = "Hip Hop / Rap"
    Schlager = "Schlager"
    ExtremeMetal = "Extreme Metal"
    Metal = "Metal"
    Afro = "Afro"
    Others = "Others"


class SpotifyTrack:
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    MODE_STRINGS = ["Minor", "Major"]
    KEY_SIGNATURE_STRINGS = ["♮", "1♯", "2♯", "3♯", "4♯", "5♯", "6♯/6♭", "5♭", "4♭", "3♭", "2♭", "1♭"]

    SUPER_GENRES = [
        SuperGenres.Pop, SuperGenres.Rock, SuperGenres.EDM, SuperGenres.HipHopOrRap,
        SuperGenres.Schlager, SuperGenres.ExtremeMetal, SuperGenres.Metal, SuperGenres.Afro,
        SuperGenres.Others
    ]

    ACCEPTED_GENRE_SUBSTRINGS_BY_SUPER_GENRE = {
        SuperGenres.Pop: ["pop", "new romantic", "wave", "girl group", "boy band"],
        SuperGenres.Rock: ["rock", "post-grunge", "punk", "mellow gold"],
        SuperGenres.EDM: [
            "edm", "dance", "house", "trance", "techno", "hands up", "hardstyle", "big room",
            "dubstep", "brostep", "complextro", "disco", "hi-nrg", "dancefloor", "drum and bass", "dnb",
            "jungle", "melbourne bounce"
        ],
        SuperGenres.HipHopOrRap: ["hip hop", "rap", "trap", "drill"],
        SuperGenres.Schlager: ["schlager"],
        SuperGenres.ExtremeMetal: ["black metal", "death metal", "melodeath"],
        SuperGenres.Metal: ["metal", "neue deutsche harte", "industrial", "screamo", "emo", "nwobhm"],
        SuperGenres.Afro: ["afro", "r&b", "soul", "reggae", "funk", "urban", "dancehall"],
        SuperGenres.Others: []
    }

    def __init__(self):
        self.id = None
        self.artist_ids = []
        self.artists = []
        self.title = None
        self.added_by_user_id = None
        self.added_by = None
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
        for super_genre in SpotifyTrack.SUPER_GENRES:
            accepted_genre_substrings = SpotifyTrack.ACCEPTED_GENRE_SUBSTRINGS_BY_SUPER_GENRE[super_genre]
            for accepted_genre_substring in accepted_genre_substrings:
                if accepted_genre_substring in genre:
                    return super_genre

        return SuperGenres.Others

    # TODOLATER #234 Refactor: Keep key signature as number in API, convert to string in App
    @staticmethod
    def __get_key_signature_from_key_and_mode(key, mode):
        if (key == Keys.C and mode == Modes.Major) or (key == Keys.A and mode == Modes.Minor):
            return "♮"
        if (key == Keys.G and mode == Modes.Major) or (key == Keys.E and mode == Modes.Minor):
            return "1♯"
        if (key == Keys.D and mode == Modes.Major) or (key == Keys.B and mode == Modes.Minor):
            return "2♯"
        if (key == Keys.A and mode == Modes.Major) or (key == Keys.Fs and mode == Modes.Minor):
            return "3♯"
        if (key == Keys.E and mode == Modes.Major) or (key == Keys.Cs and mode == Modes.Minor):
            return "4♯"
        if (key == Keys.B and mode == Modes.Major) or (key == Keys.Gs and mode == Modes.Minor):
            return "5♯"
        if (key == Keys.Fs and mode == Modes.Major) or (key == Keys.Ds and mode == Modes.Minor):
            return "6♯/6♭"
        if (key == Keys.Cs and mode == Modes.Major) or (key == Keys.As and mode == Modes.Minor):
            return "5♭"
        if (key == Keys.Gs and mode == Modes.Major) or (key == Keys.F and mode == Modes.Minor):
            return "4♭"
        if (key == Keys.Ds and mode == Modes.Major) or (key == Keys.C and mode == Modes.Minor):
            return "3♭"
        if (key == Keys.As and mode == Modes.Major) or (key == Keys.G and mode == Modes.Minor):
            return "2♭"
        if (key == Keys.F and mode == Modes.Major) or (key == Keys.D and mode == Modes.Minor):
            return "1♭"

        return "n/a"

    @staticmethod
    def __process_audio_feature_value(value):
        return round(value * 100)
