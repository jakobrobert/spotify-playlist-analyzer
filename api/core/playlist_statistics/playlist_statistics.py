import statistics

from core.playlist_statistics.attribute_distribution_interval import AttributeDistributionInterval
from core.spotify.spotify_track import SpotifyTrack
from core.utils import Utils


LOG_PREFIX = "PlaylistStatistics."


class PlaylistStatistics:
    def __init__(self, tracks):
        self.tracks = tracks

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_total_duration_ms(self):
        if not self.tracks:
            return 0.0

        return sum(track.duration_ms for track in self.tracks)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_duration_ms(self):
        return self.__get_average_of_attribute("duration_ms")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_popularity(self):
        return self.__get_average_of_attribute("popularity")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_release_year(self):
        return self.__get_average_of_attribute("release_year")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_tempo(self):
        return self.__get_average_of_attribute("tempo")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_speechiness(self):
        return self.__get_average_of_attribute("speechiness")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_liveness(self):
        return self.__get_average_of_attribute("liveness")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_acousticness(self):
        return self.__get_average_of_attribute("acousticness")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_instrumentalness(self):
        return self.__get_average_of_attribute("instrumentalness")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_valence(self):
        return self.__get_average_of_attribute("valence")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_energy(self):
        return self.__get_average_of_attribute("energy")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_average_danceability(self):
        return self.__get_average_of_attribute("danceability")

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_duration_distribution_items(self):
        first_interval_max_duration = 120000  # 120 seconds -> 02:00
        last_interval_min_duration = 300000  # 300 seconds -> 05:00
        interval_size = 30000  # 30 seconds

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_duration, last_interval_min_duration, interval_size,
            lambda track: track.duration_ms)

        return self.__convert_attribute_distribution_intervals_to_dicts_with_label(
            intervals, lambda duration_ms: PlaylistStatistics.__get_duration_string(duration_ms))

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_release_year_distribution_items(self):
        first_interval_max_year = 1979
        last_interval_min_year = 2020
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_year, last_interval_min_year, interval_size,
            lambda track: track.release_year)

        return self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_popularity_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.popularity)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_super_genres_distribution_items(self):
        items = []

        # Calculate count for each super genre
        for super_genre in SpotifyTrack.SUPER_GENRES:
            count = 0

            for track in self.tracks:
                if super_genre in track.super_genres:
                    count += 1

            item = {
                "label": super_genre,
                "count": count
            }

            items.append(item)

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(items, total_count)

        return items

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_tempo_distribution_items(self):
        first_interval_max_tempo = 89
        last_interval_min_tempo = 180
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_tempo, last_interval_min_tempo, interval_size,
            lambda track: track.tempo)

        return self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_key_distribution_items(self):
        # TODOLATER merge loops into one, similar to get_super_genres_distribution_items.
        #  -> maybe can then extract general helper method for categorical values?
        items = []

        # Add one item for each key
        for key_name in SpotifyTrack.KEY_STRINGS:
            item = {
                "label": key_name,
                "count": 0
            }

            items.append(item)

        # Calculate count for each key
        for track in self.tracks:
            item = items[track.key]
            item["count"] += 1

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(items, total_count)

        return items

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_mode_distribution_items(self):
        # TODOLATER merge loops into one, similar to get_super_genres_distribution_items
        #  -> maybe can then extract general helper method for categorical values?
        items = []

        # Add one item for each mode
        for mode_name in SpotifyTrack.MODE_STRINGS:
            item = {
                "label": mode_name,
                "count": 0
            }

            items.append(item)

        # Calculate count for each mode
        for track in self.tracks:
            item = items[track.mode]
            item["count"] += 1

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(items, total_count)

        return items

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_key_signature_distribution_items(self):
        # TODOLATER merge loops into one, similar to get_super_genres_distribution_items
        #  -> maybe can then extract general helper method for categorical values?
        items = []

        # Add one item for each key_signature
        for key_signature_name in SpotifyTrack.KEY_SIGNATURE_STRINGS:
            item = {
                "label": key_signature_name,
                "count": 0
            }

            items.append(item)

        # Calculate count for each key_signature
        for track in self.tracks:
            key_signature = track.key_signature
            key_signature_index = SpotifyTrack.KEY_SIGNATURE_STRINGS.index(key_signature)
            item = items[key_signature_index]
            item["count"] += 1

        # Calculate percentages based on counts
        total_count = len(self.tracks)
        PlaylistStatistics.__add_percentages_to_attribute_distribution_items(items, total_count)

        return items

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_loudness_distribution_items(self):
        first_interval_max_loudness = -16
        last_interval_min_loudness = -2
        interval_size = 2

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max_loudness, last_interval_min_loudness, interval_size,
            lambda track: track.loudness)

        return self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_danceability_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.danceability)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_energy_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.energy)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_speechiness_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.speechiness)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_liveness_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.liveness)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_acousticness_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.acousticness)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_instrumentalness_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.instrumentalness)

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_valence_distribution_items(self):
        return self.__get_attribute_distribution_items_for_interval_range_0_to_100(lambda track: track.valence)

    def __get_average_of_attribute(self, attribute):
        if not self.tracks:
            return None

        return statistics.mean(getattr(track, attribute) for track in self.tracks)

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

    def __get_attribute_distribution_items_for_interval_range_0_to_100(self, get_attribute_value_of_track):
        first_interval_max = 9
        last_interval_min = 90
        interval_size = 10

        intervals = self.__get_attribute_distribution_intervals(
            first_interval_max, last_interval_min, interval_size, get_attribute_value_of_track)

        return self.__convert_attribute_distribution_intervals_to_dicts_with_label(intervals)

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
