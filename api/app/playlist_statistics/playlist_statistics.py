from spotify.spotify_track import SpotifyTrack
from playlist_statistics.attribute_distribution_interval import AttributeDistributionInterval


class PlaylistStatistics:
    def __init__(self, tracks):
        self.tracks = tracks

    def get_total_duration_ms(self):
        total_duration_ms = 0

        for track in self.tracks:
            total_duration_ms += track.duration_ms

        return total_duration_ms

    def get_average_duration_ms(self):
        if not self.tracks:
            return None

        return self.get_total_duration_ms() / len(self.tracks)

    def get_average_popularity(self):
        if not self.tracks:
            return None

        total_popularity = 0.0

        for track in self.tracks:
            total_popularity += track.popularity

        return total_popularity / len(self.tracks)

    def get_average_release_year(self):
        if not self.tracks:
            return None

        total_year = 0.0

        for track in self.tracks:
            total_year += track.release_year

        return total_year / len(self.tracks)

    def get_average_tempo(self):
        if not self.tracks:
            return None

        total_tempo = 0.0

        for track in self.tracks:
            total_tempo += track.tempo

        return total_tempo / len(self.tracks)

    def get_duration_distribution_items(self):
        first_interval_max_duration = 120000  # 120 seconds -> 02:00
        last_interval_min_duration = 300000  # 300 seconds -> 05:00
        interval_size = 30000  # 30 seconds

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_duration, last_interval_min_duration, interval_size,
            lambda track: track.duration_ms)

        # TODO can inline returns
        # TODO fix: pass get_label_for_value lambda
        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_release_year_distribution_items(self):
        first_interval_max_year = 1979
        last_interval_min_year = 2020
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_year, last_interval_min_year, interval_size,
            lambda track: track.release_year)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_popularity_distribution_items(self):
        first_interval_max_popularity = 9
        last_interval_min_popularity = 90
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_popularity, last_interval_min_popularity, interval_size,
            lambda track: track.popularity)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_tempo_distribution_items(self):
        first_interval_max_tempo = 89
        last_interval_min_tempo = 180
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_tempo, last_interval_min_tempo, interval_size,
            lambda track: track.tempo)

        dicts_with_label = self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

        return dicts_with_label

    def get_key_distribution_items(self):
        key_distribution_items = []

        # Add one item for each key
        for key_name in SpotifyTrack.KEY_STRINGS:
            key_with_count = {
                "label": key_name,
                "count": 0
            }

            key_distribution_items.append(key_with_count)

        # Calculate count for each key
        for track in self.tracks:
            key_with_count = key_distribution_items[track.key]
            key_with_count["count"] += 1

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(key_distribution_items, total_count)

        return key_distribution_items

    def get_mode_distribution_items(self):
        mode_distribution_items = []

        # Add one item for each mode
        for mode_name in SpotifyTrack.MODE_STRINGS:
            mode_with_count = {
                "label": mode_name,
                "count": 0
            }

            mode_distribution_items.append(mode_with_count)

        # Calculate count for each mode
        for track in self.tracks:
            mode_with_count = mode_distribution_items[track.mode]
            mode_with_count["count"] += 1

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(mode_distribution_items, total_count)

        return mode_distribution_items

    def get_key_signature_distribution_items(self):
        key_signature_distribution_items = []

        # Add one item for each key_signature
        for key_signature_name in SpotifyTrack.KEY_SIGNATURE_STRINGS:
            key_signature_with_count = {
                "label": key_signature_name,
                "count": 0
            }

            key_signature_distribution_items.append(key_signature_with_count)

        # Calculate count for each key_signature
        for track in self.tracks:
            key_signature = track.key_signature
            key_signature_index = SpotifyTrack.KEY_SIGNATURE_STRINGS.index(key_signature)
            key_signature_with_count = key_signature_distribution_items[key_signature_index]
            key_signature_with_count["count"] += 1

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(key_signature_distribution_items, total_count)

        return key_signature_distribution_items

    def __get_attribute_distribution_intervals(
            self, first_interval_max, last_interval_min, interval_size, get_attribute_value_of_track):

        all_intervals = []

        all_intervals.append(PlaylistStatistics.__create_first_interval(first_interval_max))
        all_intervals.extend(
            PlaylistStatistics.__create_middle_intervals(first_interval_max, last_interval_min, interval_size))
        all_intervals.append(PlaylistStatistics.__create_last_interval(last_interval_min))

        all_values = [get_attribute_value_of_track(track) for track in self.tracks]

        for interval in all_intervals:
            interval.update_count(all_values)

        total_count = len(self.tracks)
        for interval in all_intervals:
            interval.update_percentage(total_count)

        return all_intervals

    @staticmethod
    def __create_first_interval(first_interval_max):
        return AttributeDistributionInterval(None, first_interval_max)

    @staticmethod
    def __create_middle_intervals(first_interval_max, last_interval_min, interval_size):
        middle_intervals = []

        for min_value in range(first_interval_max + 1, last_interval_min, interval_size):
            max_value = min_value + interval_size - 1
            middle_intervals.append(AttributeDistributionInterval(min_value, max_value))

        return middle_intervals

    @staticmethod
    def __create_last_interval(last_interval_min):
        return AttributeDistributionInterval(last_interval_min, None)

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

    # This is used for categorical values like key & mode. There, cannot use AttributeDistributionInterval.
    @staticmethod
    def __add_percentages_to_attribute_distribution_items(attribute_distribution_items, total_count):
        for item in attribute_distribution_items:
            if total_count == 0:
                item["percentage"] = 0
                continue

            item["percentage"] = 100 * item["count"] / total_count
