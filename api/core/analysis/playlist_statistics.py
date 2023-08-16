import statistics

LOG_PREFIX = "PlaylistStatistics."


class PlaylistStatistics:
    def __init__(self, tracks):
        self.tracks = tracks

    # REMARK NO need to measure performance of get_total_duration_ms, get_average_duration_ms, etc.
    # -> Only take a few ms each with hundreds of tracks
    # -> Not significant in comparison to requests in SpotifyApiClient which take several seconds in total
    def get_total_duration_ms(self):
        if not self.tracks:
            return 0.0

        return sum(track.duration_ms for track in self.tracks)

    def get_average_duration_ms(self):
        return self.__get_average_of_attribute("duration_ms")

    def get_average_popularity(self):
        return self.__get_average_of_attribute("popularity")

    def get_average_release_year(self):
        return self.__get_average_of_attribute("release_year")

    def get_average_tempo(self):
        return self.__get_average_of_attribute("tempo")

    def get_average_speechiness(self):
        return self.__get_average_of_attribute("speechiness")

    def get_average_liveness(self):
        return self.__get_average_of_attribute("liveness")

    def get_average_acousticness(self):
        return self.__get_average_of_attribute("acousticness")

    def get_average_instrumentalness(self):
        return self.__get_average_of_attribute("instrumentalness")

    def get_average_valence(self):
        return self.__get_average_of_attribute("valence")

    def get_average_energy(self):
        return self.__get_average_of_attribute("energy")

    def get_average_danceability(self):
        return self.__get_average_of_attribute("danceability")

    def __get_average_of_attribute(self, attribute):
        if not self.tracks:
            return None

        return statistics.mean(getattr(track, attribute) for track in self.tracks)
