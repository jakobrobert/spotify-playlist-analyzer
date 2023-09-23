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
        self.super_genres = SuperGenreUtils.get_super_genres_for_genres(genres)

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

    @staticmethod
    def from_dict(track_dict):
        track = Track()

        track.id = track_dict["id"]
        track.artist_ids = track_dict["artist_ids"]
        track.artists = track_dict["artists"]
        track.title = track_dict["title"]
        track.added_by_user_id = track_dict["added_by_user_id"]
        track.added_by = track_dict["added_by"]
        track.duration_ms = track_dict["duration_ms"]
        track.release_year = track_dict["release_year"]
        track.popularity = track_dict["popularity"]
        track.genres = track_dict["genres"]
        track.super_genres = track_dict["super_genres"]
        track.tempo = track_dict["tempo"]
        track.key = track_dict["key"]
        track.mode = track_dict["mode"]
        track.key_and_mode_pair = track_dict["key_and_mode_pair"]
        track.key_signature = track_dict["key_signature"]
        track.loudness = track_dict["loudness"]
        track.danceability = track_dict["danceability"]
        track.energy = track_dict["energy"]
        track.valence = track_dict["valence"]
        track.instrumentalness = track_dict["instrumentalness"]
        track.acousticness = track_dict["acousticness"]
        track.liveness = track_dict["liveness"]
        track.speechiness = track_dict["speechiness"]

        return track

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
