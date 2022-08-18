import json

# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    def get_total_duration_ms(self):
        total_duration_ms = 0

        for track in self.tracks:
            total_duration_ms += track.duration_ms

        return total_duration_ms

    def get_average_duration_ms(self):
        return self.get_total_duration_ms() / len(self.tracks)

    def get_average_popularity(self):
        total_popularity = 0.0

        for track in self.tracks:
            total_popularity += track.popularity

        return total_popularity / len(self.tracks)

    def get_average_release_year(self):
        total_year = 0.0

        for track in self.tracks:
            total_year += track.release_year

        return total_year / len(self.tracks)

    def get_average_tempo(self):
        total_tempo = 0.0

        for track in self.tracks:
            total_tempo += track.tempo

        return total_tempo / len(self.tracks)

    def get_duration_interval_to_percentage(self):
        first_interval_max_duration = 120000    # 120 seconds -> 02:00
        last_interval_min_duration = 300000     # 300 seconds -> 05:00
        interval_size = 30000                   # 30 seconds

        duration_intervals_with_count = self.__get_intervals_with_count(
            first_interval_max_duration, last_interval_min_duration, interval_size,
            lambda track: track.duration_ms, lambda duration_ms: SpotifyPlaylist.__get_duration_string(duration_ms))

        return self.__convert_counts_to_percentages(duration_intervals_with_count)

    def get_release_year_interval_to_percentage(self):
        first_interval_max_year = 1969
        last_interval_min_year = 2020
        interval_size = 10

        year_intervals_with_count = self.__get_intervals_with_count(
            first_interval_max_year, last_interval_min_year, interval_size, lambda track: track.release_year)

        return self.__convert_counts_to_percentages(year_intervals_with_count)

    def get_popularity_interval_to_percentage(self):
        first_interval_max_popularity = 9
        last_interval_min_popularity = 90
        interval_size = 10

        popularity_intervals_with_count = self.__get_intervals_with_count(
            first_interval_max_popularity, last_interval_min_popularity, interval_size, lambda track: track.popularity)

        return self.__convert_counts_to_percentages(popularity_intervals_with_count)

    def get_tempo_interval_to_percentage(self):
        first_interval_max_tempo = 89
        last_interval_min_tempo = 180
        interval_size = 10

        tempo_intervals_with_count = self.__get_intervals_with_count(
            first_interval_max_tempo, last_interval_min_tempo, interval_size, lambda track: track.tempo)

        return self.__convert_counts_to_percentages(tempo_intervals_with_count)

    def get_key_to_percentage(self):
        keys_with_count = []

        # Add one item for each key
        for key_name in SpotifyTrack.KEY_STRINGS:
            key_with_count = {
                "label": key_name,
                "count": 0
            }

            keys_with_count.append(key_with_count)

        # Calculate count for each key
        for track in self.tracks:
            key_with_count = keys_with_count[track.key]
            key_with_count["count"] += 1

        return self.__convert_counts_to_percentages(keys_with_count)

    def get_mode_to_percentage(self):
        modes_with_count = []

        # Add one item for each mode
        for mode_name in SpotifyTrack.MODE_STRINGS:
            mode_with_count = {
                "label": mode_name,
                "count": 0
            }

            modes_with_count.append(mode_with_count)

        # Calculate count for each mode
        for track in self.tracks:
            mode_with_count = modes_with_count[track.mode]
            mode_with_count["count"] += 1

        return self.__convert_counts_to_percentages(modes_with_count)

    def __get_intervals_with_count(self, first_interval_max, last_interval_min, interval_size,
                                   get_track_value, get_label_for_value=None):
        intervals = []

        if get_label_for_value is None:
            get_label_for_value = str

        # First interval
        first_interval = {
            "label": f"≤ {get_label_for_value(first_interval_max)}",
            "count": 0
        }

        for track in self.tracks:
            if get_track_value(track) <= first_interval_max:
                first_interval["count"] += 1

        intervals.append(first_interval)

        # Middle intervals
        for min_value in range(first_interval_max + 1, last_interval_min, interval_size):
            max_value = min_value + interval_size - 1
            interval = {
                "label": f"{get_label_for_value(min_value)} - {get_label_for_value(max_value)}",
                "count": 0
            }

            for track in self.tracks:
                if min_value <= get_track_value(track) <= max_value:
                    interval["count"] += 1

            intervals.append(interval)

        # Last interval
        last_interval = {
            "label": f"≥ {get_label_for_value(last_interval_min)}",
            "count": 0
        }

        for track in self.tracks:
            if get_track_value(track) >= last_interval_min:
                last_interval["count"] += 1

        intervals.append(last_interval)

        return intervals

    def __convert_counts_to_percentages(self, intervals_with_count):
        intervals_with_percentage = []

        for interval_with_count in intervals_with_count:
            proportion = interval_with_count["count"] / len(self.tracks)
            percentage = proportion * 100.0

            interval_with_percentage = {
                "label": interval_with_count["label"],
                "percentage": percentage
            }

            intervals_with_percentage.append(interval_with_percentage)

        return intervals_with_percentage

    @staticmethod
    def __get_duration_string(duration_ms):
        total_seconds = duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
