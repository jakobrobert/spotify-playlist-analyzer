from core.analysis.super_genre_utils import SuperGenreUtils


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


class KeyAndModePairs:
    C_MINOR = 0
    Cs_MINOR = 1
    D_MINOR = 2
    Ds_MINOR = 3
    E_MINOR = 4
    F_MINOR = 5
    Fs_MINOR = 6
    G_MINOR = 7
    Gs_MINOR = 8
    A_MINOR = 9
    Bb_MINOR = 10
    B_MINOR = 11

    C_MAJOR = 12
    Db_MAJOR = 13
    D_MAJOR = 14
    Eb_MAJOR = 15
    E_MAJOR = 16
    F_MAJOR = 17
    Gb_MAJOR = 18
    G_MAJOR = 19
    Ab_MAJOR = 20
    A_MAJOR = 21
    Bb_MAJOR = 22
    B_MAJOR = 23


class Track:
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    MODE_STRINGS = ["Minor", "Major"]
    KEY_AND_MODE_PAIR_STRINGS = [
        "C Minor", "C# Minor", "D Minor", "D# Minor", "E Minor", "F Minor",
        "F# Minor", "G Minor", "G# Minor", "A Minor", "Bb Minor", "B Minor",
        "C Major", "Db Major", "D Major", "Eb Major", "E Major", "F Major",
        "Gb Major", "G Major", "Ab Major", "A Major", "Bb Major", "B Major"
    ]
    KEY_SIGNATURE_STRINGS = ["♮", "1♯", "2♯", "3♯", "4♯", "5♯", "6♯/6♭", "5♭", "4♭", "3♭", "2♭", "1♭"]

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
        self.key_and_mode_pair = -1
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
        self.key_and_mode_pair = Track.__get_key_and_mode_pair(self.key, self.mode)
        self.key_signature = Track.__get_key_signature_from_key_and_mode(self.key, self.mode)
        self.loudness = audio_features["loudness"]
        self.danceability = Track.__process_audio_feature_value(audio_features["danceability"])
        self.energy = Track.__process_audio_feature_value(audio_features["energy"])
        self.valence = Track.__process_audio_feature_value(audio_features["valence"])
        self.instrumentalness = Track.__process_audio_feature_value(audio_features["instrumentalness"])
        self.acousticness = Track.__process_audio_feature_value(audio_features["acousticness"])
        self.liveness = Track.__process_audio_feature_value(audio_features["liveness"])
        self.speechiness = Track.__process_audio_feature_value(audio_features["speechiness"])

    def __update_super_genres_by_genres(self, genres):
        super_genres_for_this_track = []
        for genre in genres:
            super_genre = SuperGenreUtils.get_super_genre_for_genre(genre)
            if super_genre not in self.super_genres:
                super_genres_for_this_track.append(super_genre)

        sorted_super_genres = []
        for super_genre in SuperGenreUtils.SUPER_GENRES:
            if super_genre in super_genres_for_this_track:
                sorted_super_genres.append(super_genre)

        self.super_genres = sorted_super_genres

    @staticmethod
    def __get_key_and_mode_pair(key, mode):
        if mode == Modes.Minor:
            return key

        if mode == Modes.Major:
            return key + 12

        return -1

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
