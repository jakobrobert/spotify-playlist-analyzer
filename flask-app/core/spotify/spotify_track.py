from core.utils import Utils


class SpotifyTrack:
    KEY_STRINGS = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    MODE_STRINGS = ["Minor", "Major"]

    def __init__(self):
        self.id = "n/a"
        self.artist_ids = []
        self.artists = []
        self.title = "n/a"
        self.added_by = "n/a"
        self.duration_ms = 0
        self.release_year = 0
        self.popularity = 0
        self.genres = []
        self.super_genres = []
        self.tempo = 0
        self.key = -1
        self.mode = -1
        self.key_signature = "n/a"
        self.loudness = 0
        self.danceability = 0
        self.energy = 0
        self.valence = 0
        self.instrumentalness = 0
        self.acousticness = 0
        self.liveness = 0
        self.speechiness = 0

    def get_artists_string(self):
        return ", ".join(self.artists)

    def get_duration_string(self):
        return Utils.convert_duration_to_string(self.duration_ms)

    def get_genres_string(self):
        return ", ".join(self.genres)

    def get_super_genres_string(self):
        return ", ".join(self.super_genres)

    def get_tempo_string(self):
        return f"{self.tempo:.1f}"

    def get_key_string(self):
        return SpotifyTrack.__get_from_list(SpotifyTrack.KEY_STRINGS, self.key)

    def get_mode_string(self):
        return SpotifyTrack.__get_from_list(SpotifyTrack.MODE_STRINGS, self.mode)

    def get_loudness_string(self):
        return f"{self.loudness:.1f}"

    @staticmethod
    def __get_from_list(_list, index):
        if index < 0 or index >= len(_list):
            return "n/a"

        return _list[index]
