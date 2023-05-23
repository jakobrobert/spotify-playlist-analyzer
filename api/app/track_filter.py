class TrackFilter:
    @staticmethod
    def filter_tracks(tracks, filter_params):
        filter_by = filter_params["filter_by"]

        if filter_by is None:
            return tracks

        if filter_by == "artists":
            artists_substring = filter_params["artists_substring"]
            return list(
                filter(lambda track: TrackFilter.__filter_accepts_string(track.artists, artists_substring), tracks))

        if filter_by == "title":
            title_substring = filter_params["title_substring"]
            return list(filter(lambda track: TrackFilter.__filter_accepts_title(track.title, title_substring), tracks))

        if filter_by == "release_year":
            min_release_year = filter_params["min_release_year"]
            max_release_year = filter_params["max_release_year"]
            return list(filter(lambda track: min_release_year <= track.release_year <= max_release_year, tracks))

        if filter_by == "tempo":
            min_tempo = filter_params["min_tempo"]
            max_tempo = filter_params["max_tempo"]
            return list(filter(lambda track: min_tempo <= track.tempo <= max_tempo, tracks))

        if filter_by == "key":
            expected_key = filter_params["expected_key"]
            return list(filter(lambda track: track.get_key_string() == expected_key, tracks))

        if filter_by == "mode":
            expected_mode = filter_params["expected_mode"]
            return list(filter(lambda track: track.get_mode_string() == expected_mode, tracks))

        if filter_by == "key_signature":
            expected_key_signature = filter_params["expected_key_signature"]
            return list(filter(lambda track: track.key_signature == expected_key_signature, tracks))

        if filter_by == "genres":
            genres_substring = filter_params["genres_substring"]
            return list(filter(lambda track: TrackFilter.__filter_accepts_string(track.genres, genres_substring), tracks))

        raise ValueError(f"This attribute is not supported to filter by: {filter_by}")

    @staticmethod
    def __filter_accepts_string(actual_strings, expected_substring):
        # Ignore case & spaces
        actual_strings_processed = [TrackFilter.__process_string_for_filter(string) for string in actual_strings]
        expected_substring_processed = TrackFilter.__process_string_for_filter(expected_substring)

        return any(expected_substring_processed in artist for artist in actual_strings_processed)

    @staticmethod
    def __filter_accepts_title(actual_title, expected_title_substring):
        # Ignore case & spaces
        actual_title_processed = TrackFilter.__process_string_for_filter(actual_title)
        expected_title_substring_processed = TrackFilter.__process_string_for_filter(expected_title_substring)

        return expected_title_substring_processed in actual_title_processed

    @staticmethod
    def __process_string_for_filter(original_string):
        return original_string.lower().replace(" ", "")
