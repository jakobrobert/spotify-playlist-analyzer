class TrackFilter:
    # TODO reduce number of function params by grouping params into a dict
    @staticmethod
    def filter_tracks(
            tracks, filter_by,
            artists_substring, title_substring, min_release_year, max_release_year, min_tempo, max_tempo,
            expected_key, expected_mode, expected_key_signature, genres_substring
    ):
        if filter_by is None:
            return tracks

        if filter_by == "artists":
            if artists_substring is None:
                raise ValueError("artists_substring must be defined to filter by artists!")

            return list(
                filter(lambda track: TrackFilter.__filter_accepts_string(track.artists, artists_substring), tracks))

        if filter_by == "title":
            if title_substring is None:
                raise ValueError("title_substring must be defined to filter by title!")

            return list(filter(lambda track: TrackFilter.__filter_accepts_title(track.title, title_substring), tracks))

        if filter_by == "release_year":
            if min_release_year is None:
                raise ValueError("min_release_year must be defined to filter by release_year!")

            if max_release_year is None:
                raise ValueError("max_release_year must be defined to filter by release_year!")

            return list(filter(lambda track: min_release_year <= track.release_year <= max_release_year, tracks))

        if filter_by == "tempo":
            if min_tempo is None:
                raise ValueError("min_tempo must be defined to filter by tempo!")

            if max_tempo is None:
                raise ValueError("max_tempo must be defined to filter by tempo!")

            return list(filter(lambda track: min_tempo <= track.tempo <= max_tempo, tracks))

        if filter_by == "key":
            if expected_key is None:
                raise ValueError("expected_key must be defined to filter by key!")

            return list(filter(lambda track: track.get_key_string() == expected_key, tracks))

        if filter_by == "mode":
            if expected_mode is None:
                raise ValueError("expected_mode must be defined to filter by mode!")

            return list(filter(lambda track: track.get_mode_string() == expected_mode, tracks))

        if filter_by == "key_signature":
            if expected_key_signature is None:
                raise ValueError("expected_key_signature must be defined to filter by key_signature!")

            return list(filter(lambda track: track.key_signature == expected_key_signature, tracks))

        if filter_by == "genres":
            if genres_substring is None:
                raise ValueError("genres_substring must be defined to filter by genres!")

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
