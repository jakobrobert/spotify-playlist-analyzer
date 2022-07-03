import json

# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    # TODO in API, can be static. but first clarify: should string conversion be done in API or on client side?
    # Cannot be static, else template code cannot access it
    def percentage_to_string(self, percentage):
        return f"{percentage:.1f}"

    def get_total_duration_ms(self):
        total_duration_ms = 0

        for track in self.tracks:
            total_duration_ms += track.duration_ms

        return total_duration_ms

    def get_total_duration_string(self):
        total_milliseconds = self.get_total_duration_ms()
        total_seconds = total_milliseconds // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60

        return f"{total_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"

    def get_average_duration_ms(self):
        return self.get_total_duration_ms() / len(self.tracks)

    def get_average_duration_string(self):
        average_duration_ms = int(self.get_average_duration_ms())

        return SpotifyTrack.get_duration_string_helper(average_duration_ms)

    def get_average_release_year(self):
        total_year = 0.0

        for track in self.tracks:
            total_year += track.release_year

        return total_year / len(self.tracks)

    def get_average_release_year_string(self):
        average_year = self.get_average_release_year()

        return f"{average_year:.1f}"

    def get_average_tempo(self):
        total_tempo = 0.0

        for track in self.tracks:
            total_tempo += track.tempo

        return total_tempo / len(self.tracks)

    def get_average_tempo_string(self):
        average_tempo = self.get_average_tempo()

        return f"{average_tempo:.1f}"

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

