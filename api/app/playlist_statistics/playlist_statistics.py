from spotify.spotify_track import SpotifyTrack
from playlist_statistics.attribute_distribution_interval import AttributeDistributionInterval


class PlaylistStatistics:
    def __init__(self, tracks):
        self.tracks = tracks

    def get_duration_interval_to_percentage(self):
        first_interval_max_duration = 120000  # 120 seconds -> 02:00
        last_interval_min_duration = 300000  # 300 seconds -> 05:00
        interval_size = 30000  # 30 seconds

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_duration, last_interval_min_duration, interval_size,
            lambda track: track.duration_ms)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_release_year_interval_to_percentage(self):
        first_interval_max_year = 1979
        last_interval_min_year = 2020
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_year, last_interval_min_year, interval_size,
            lambda track: track.release_year)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_popularity_interval_to_percentage(self):
        first_interval_max_popularity = 9
        last_interval_min_popularity = 90
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_popularity, last_interval_min_popularity, interval_size,
            lambda track: track.popularity)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_tempo_interval_to_percentage(self):
        first_interval_max_tempo = 89
        last_interval_min_tempo = 180
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_tempo, last_interval_min_tempo, interval_size,
            lambda track: track.tempo)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

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

    def get_key_signature_to_percentage(self):
        key_signatures_with_count = []

        # Add one item for each key_signature
        for key_signature_name in SpotifyTrack.KEY_SIGNATURE_STRINGS:
            key_signature_with_count = {
                "label": key_signature_name,
                "count": 0
            }

            key_signatures_with_count.append(key_signature_with_count)

        # Calculate count for each key_signature
        for track in self.tracks:
            key_signature = track.key_signature
            key_signature_index = SpotifyTrack.KEY_SIGNATURE_STRINGS.index(key_signature)
            key_signature_with_count = key_signatures_with_count[key_signature_index]
            key_signature_with_count["count"] += 1

        return self.__convert_counts_to_percentages(key_signatures_with_count)

    def __get_attribute_distribution_intervals(
            self, first_interval_max, last_interval_min, interval_size, get_attribute_value_of_track):

        intervals = []

        # TODO Rather than using section comments, extract into helper methods for first interval, middle intervals, last interval
        # First interval
        first_interval = AttributeDistributionInterval(None, first_interval_max)

        # TODO can extract general method is_attribute_value_in_range into AttributeDistributionInterval
        #   -> special handling for first & last interval by checking for None
        for track in self.tracks:
            if get_attribute_value_of_track(track) <= first_interval_max:
                first_interval.count += 1

        intervals.append(first_interval)

        # Middle intervals
        for min_value in range(first_interval_max + 1, last_interval_min, interval_size):
            max_value = min_value + interval_size - 1
            interval = AttributeDistributionInterval(min_value, max_value)

            for track in self.tracks:
                if min_value <= get_attribute_value_of_track(track) <= max_value:
                    interval.count += 1

            intervals.append(interval)

        # Last interval
        last_interval = AttributeDistributionInterval(last_interval_min, None)

        for track in self.tracks:
            if get_attribute_value_of_track(track) >= last_interval_min:
                last_interval.count += 1

        intervals.append(last_interval)

        total_count = len(self.tracks)
        for interval in intervals:
            interval.update_percentage(total_count)

        return intervals

    # TODO Still keep this method for key & mode, there it works differently, cannot use AttributeDistributionInterval
    # TODO can pass total (len(self.tracks)), then can make it static
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
    def __convert_attribute_distribution_intervals_to_dicts_with_label(intervals, get_label_for_value=None):
        dicts_with_label = []

        # By default, for labels just convert the value to string
        if get_label_for_value is None:
            get_label_for_value = str

        for interval in intervals:
            dict_with_label = {
                "label": PlaylistStatistics.__get_label_for_interval(
                    interval.min_value, interval.max_value, get_label_for_value),
                "count": interval.count,
                "percentage": interval.percentage
            }
            dicts_with_label.append(dict_with_label)

        return dicts_with_label

    @staticmethod
    def __get_label_for_interval(min_value, max_value, get_label_for_value):
        if min_value is None:
            return f"≤ {get_label_for_value(max_value)}"

        if max_value is None:
            return f"≥ {get_label_for_value(min_value)}"

        return f"{get_label_for_value(min_value)} - {get_label_for_value(max_value)}"

    @staticmethod
    def __get_duration_string(duration_ms):
        total_seconds = duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
