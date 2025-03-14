LOG_PREFIX = "TrackFilter."


class TrackFilter:
    NUMERICAL_ATTRIBUTES = [
        "release_year", "popularity",
        
        # Audio Features
        "tempo", "loudness", "danceability", "energy", "valence",
        "instrumentalness", "acousticness", "liveness", "speechiness"]

    def __init__(self, tracks, filter_params):
        self.tracks = tracks
        self.filter_params = filter_params

    # REMARK NO need to measure performance here, only takes a few ms with hundreds of tracks
    # -> Not significant in comparison to requests in SpotifyApiClient which take several seconds in total
    def filter_tracks(self):
        filter_by = self.filter_params["filter_by"]

        if filter_by is None:
            return self.tracks

        if filter_by == "artists":
            return self.__filter_by_artists()

        if filter_by == "title":
            return self.__filter_by_title()

        if filter_by == "added_by":
            return self.__filter_by_added_by()

        if filter_by == "genres":
            return self.__filter_by_genres()

        if filter_by == "super_genres":
            return self.__filter_by_super_genres()

        if filter_by == "key":
            return self.__filter_by_key()

        if filter_by == "mode":
            return self.__filter_by_mode()
        
        if filter_by == "key_and_mode_pair":
            return self.__filter_by_key_and_mode_pair()

        if filter_by == "key_signature":
            return self.__filter_by_key_signature()

        if filter_by in TrackFilter.NUMERICAL_ATTRIBUTES:
            return self.__filter_by_number_based_attribute(filter_by)

        # Here, ValueError is correct rather than HttpError because it is logic code
        # E.g., the filter_by value might also be hardcoded in a unit test
        raise ValueError(f"TrackFilter => Invalid value for 'filter_by': '{filter_by}'")

    # TODOLATER #334 Refactor duplicated code once have added tests.
    #  E.g. __filter_where_any_string_contains_substring(track.artists, artists_substring)
    def __filter_by_artists(self):
        artists_substring = self.filter_params["artists_substring"]
        return list(filter(
            lambda track: TrackFilter.__any_string_contains_substring(track.artists, artists_substring), self.tracks))

    def __filter_by_title(self):
        title_substring = self.filter_params["title_substring"]
        return list(filter(
            lambda track: TrackFilter.__string_contains_substring(track.title, title_substring), self.tracks))

    def __filter_by_added_by(self):
        added_by_substring = self.filter_params["added_by_substring"]
        return list(filter(
            lambda track: TrackFilter.__string_contains_substring(track.added_by, added_by_substring), self.tracks))

    def __filter_by_genres(self):
        genres_substring = self.filter_params["genres_substring"]
        return list(filter(
            lambda track: TrackFilter.__any_string_contains_substring(track.genres, genres_substring), self.tracks))
    
    def __filter_by_super_genres(self):
        super_genres_substring = self.filter_params["super_genres_substring"]
        return list(filter(
            lambda track: TrackFilter.__any_string_contains_substring(track.super_genres, super_genres_substring),
            self.tracks))

    def __filter_by_key(self):
        expected_key = self.filter_params["expected_key"]
        return list(filter(
            lambda track: track.key == expected_key, self.tracks))

    def __filter_by_mode(self):
        expected_mode = self.filter_params["expected_mode"]
        return list(filter(
            lambda track: track.mode == expected_mode, self.tracks))
    
    def __filter_by_key_and_mode_pair(self):
        expected_key_and_mode_pair = self.filter_params["expected_key_and_mode_pair"]
        return list(filter(
            lambda track: track.key_and_mode_pair == expected_key_and_mode_pair, self.tracks))

    def __filter_by_key_signature(self):
        expected_key_signature = self.filter_params["expected_key_signature"]
        return list(filter(
            lambda track: track.key_signature == expected_key_signature, self.tracks))

    def __filter_by_number_based_attribute(self, attribute_name):
        min_value = self.filter_params[f"min_{attribute_name}"]
        max_value = self.filter_params[f"max_{attribute_name}"]
        return list(filter(
            lambda track: min_value <= getattr(track, attribute_name) <= max_value, self.tracks))

    @staticmethod
    def __any_string_contains_substring(actual_strings, expected_substring):
        actual_strings_processed = [TrackFilter.__process_string_for_filter(string) for string in actual_strings]
        expected_substring_processed = TrackFilter.__process_string_for_filter(expected_substring)

        return any(expected_substring_processed in actual_string for actual_string in actual_strings_processed)

    @staticmethod
    def __string_contains_substring(actual_title, expected_title_substring):
        actual_title_processed = TrackFilter.__process_string_for_filter(actual_title)
        expected_title_substring_processed = TrackFilter.__process_string_for_filter(expected_title_substring)

        return expected_title_substring_processed in actual_title_processed

    @staticmethod
    def __process_string_for_filter(original_string):
        # Ignore case & spaces
        return original_string.lower().replace(" ", "")
