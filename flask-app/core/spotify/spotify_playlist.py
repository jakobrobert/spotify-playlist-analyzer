from core.spotify.spotify_playlist_statistics import SpotifyPlaylistStatistics
from core.utils import Utils


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.statistics = SpotifyPlaylistStatistics()
        self.tracks = []

    # Member method as wrapper because did not manage to access static methods in template code
    def percentage_to_string(self, percentage):
        return Utils.convert_number_to_string(percentage)

    def get_average_value_for_attribute(self, attribute):
        if attribute == "duration_ms":
            return Utils.convert_duration_to_string(self.statistics.average_duration_ms)

        # TODONOW use get_..._string methods
        if attribute == "release_year":
            return self.statistics.average_release_year
        
        if attribute == "popularity":
            return self.statistics.average_popularity
        
        if attribute == "tempo":
            return self.statistics.average_tempo
        
        if attribute == "danceability":
            return self.statistics.average_danceability
        
        if attribute == "energy":
            return self.statistics.average_energy

        if attribute == "valence":
            return self.statistics.average_valence

        if attribute == "instrumentalness":
            return self.statistics.average_instrumentalness

        if attribute == "acousticness":
            return self.statistics.average_acousticness

        if attribute == "liveness":
            return self.statistics.average_liveness

        if attribute == "speechiness":
            return self.statistics.average_speechiness
