from core.spotify_api.spotify_playlist_statistics import SpotifyPlaylistStatistics
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

    def get_average_value_as_string_for_attribute(self, attribute):
        if attribute == "duration_ms":
            return Utils.convert_duration_to_string(self.statistics.average_duration_ms)

        if attribute == "release_year":
            return self.statistics.get_average_release_year_string()
        
        if attribute == "popularity":
            return self.statistics.get_average_popularity_string()
        
        if attribute == "tempo":
            return self.statistics.get_average_tempo_string()
        
        if attribute == "danceability":
            return self.statistics.get_average_danceability_string()
        
        if attribute == "energy":
            return self.statistics.get_average_energy_string()

        if attribute == "valence":
            return self.statistics.get_average_valence_string()

        if attribute == "instrumentalness":
            return self.statistics.get_average_instrumentalness_string()

        if attribute == "acousticness":
            return self.statistics.get_average_acousticness_string()

        if attribute == "liveness":
            return self.statistics.get_average_liveness_string()

        if attribute == "speechiness":
            return self.statistics.get_average_speechiness_string()
