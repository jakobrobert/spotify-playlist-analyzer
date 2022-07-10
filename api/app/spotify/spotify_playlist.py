import json

# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    def get_release_year_interval_to_percentage(self):
        first_interval_max_year = 1969
        last_interval_min_year = 2020
        interval_size = 10

        year_interval_to_count = self.__get_attribute_interval_to_count(
            first_interval_max_year, last_interval_min_year, interval_size, lambda track: track.release_year)

        return self.__convert_counts_to_percentages(year_interval_to_count)

    def get_tempo_interval_to_percentage(self):
        first_interval_max_tempo = 89
        last_interval_min_year = 180
        interval_size = 10

        tempo_interval_to_count = self.__get_attribute_interval_to_count(
            first_interval_max_tempo, last_interval_min_year, interval_size, lambda track: track.tempo)

        return self.__convert_counts_to_percentages(tempo_interval_to_count)

    def get_key_to_percentage(self):
        key_to_count = {}

        for key_name in SpotifyTrack.KEY_NAMES:
            key_to_count[key_name] = 0

        key_to_count["n/a"] = 0

        for track in self.tracks:
            key_string = track.get_key_string()
            key_to_count[key_string] += 1

        return self.__convert_counts_to_percentages(key_to_count)

    def get_mode_to_percentage(self):
        mode_to_count = {
            "Major": 0,
            "Minor": 0,
            "n/a": 0
        }

        for track in self.tracks:
            mode_string = track.get_mode_string()
            mode_to_count[mode_string] += 1

        return self.__convert_counts_to_percentages(mode_to_count)

    def __get_attribute_interval_to_count(self, first_interval_max, last_interval_min, interval_size, get_track_value):
        interval_to_count = {}

        # First interval
        first_interval_string = f"≤ {first_interval_max}"
        interval_to_count[first_interval_string] = 0
        for track in self.tracks:
            if get_track_value(track) <= first_interval_max:
                interval_to_count[first_interval_string] += 1

        # Middle intervals
        for min_year in range(first_interval_max + 1, last_interval_min, interval_size):
            max_year = min_year + interval_size - 1
            interval_string = f"{min_year} - {max_year}"
            interval_to_count[interval_string] = 0
            for track in self.tracks:
                if min_year <= get_track_value(track) <= max_year:
                    interval_to_count[interval_string] += 1

        # Last interval
        last_interval_string = f"≥ {last_interval_min}"
        interval_to_count[last_interval_string] = 0
        for track in self.tracks:
            if get_track_value(track) >= last_interval_min:
                interval_to_count[last_interval_string] += 1

        return interval_to_count

    def __convert_counts_to_percentages(self, counts_dict):
        percentages_dict = {}

        for key, count in counts_dict.items():
            proportion = count / len(self.tracks)
            percentages_dict[key] = proportion * 100.0

        return percentages_dict
