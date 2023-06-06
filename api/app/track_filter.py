class TrackFilter:
    def __init__(self, tracks, filter_params):
        self.tracks = tracks
        self.filter_params = filter_params
    
    def filter_tracks(self):
        filter_by = self.filter_params["filter_by"]

        if filter_by is None:
            return self.tracks

        if filter_by == "artists":
            return self.__filter_tracks_by_artists()

        if filter_by == "title":
            title_substring = self.filter_params["title_substring"]
            return list(filter(lambda track: TrackFilter.__filter_accepts_title(track.title, title_substring), self.tracks))

        if filter_by == "genres":
            genres_substring = self.filter_params["genres_substring"]
            return list(filter(
                lambda track: TrackFilter.__filter_accepts_string(track.genres, genres_substring), self.tracks))

        if filter_by == "key":
            expected_key = self.filter_params["expected_key"]
            return list(filter(lambda track: track.get_key_string() == expected_key, self.tracks))

        if filter_by == "mode":
            expected_mode = self.filter_params["expected_mode"]
            return list(filter(lambda track: track.get_mode_string() == expected_mode, self.tracks))

        if filter_by == "key_signature":
            expected_key_signature = self.filter_params["expected_key_signature"]
            return list(filter(lambda track: track.key_signature == expected_key_signature, self.tracks))

        if filter_by == "release_year":
            min_release_year = self.filter_params["min_release_year"]
            max_release_year = self.filter_params["max_release_year"]
            return list(filter(lambda track: min_release_year <= track.release_year <= max_release_year, self.tracks))

        if filter_by == "tempo":
            min_tempo = self.filter_params["min_tempo"]
            max_tempo = self.filter_params["max_tempo"]
            return list(filter(lambda track: min_tempo <= track.tempo <= max_tempo, self.tracks))

        raise ValueError(f"This attribute is not supported to filter by: {filter_by}")

    def __filter_tracks_by_artists(self):
        artists_substring = self.filter_params["artists_substring"]
        return list(
            filter(lambda track: TrackFilter.__filter_accepts_string(track.artists, artists_substring), self.tracks))

    @staticmethod
    def __filter_accepts_string(actual_strings, expected_substring):
        actual_strings_processed = [TrackFilter.__process_string_for_filter(string) for string in actual_strings]
        expected_substring_processed = TrackFilter.__process_string_for_filter(expected_substring)

        # TODO adjust names
        return any(expected_substring_processed in artist for artist in actual_strings_processed)

    @staticmethod
    def __filter_accepts_title(actual_title, expected_title_substring):
        actual_title_processed = TrackFilter.__process_string_for_filter(actual_title)
        expected_title_substring_processed = TrackFilter.__process_string_for_filter(expected_title_substring)

        return expected_title_substring_processed in actual_title_processed

    @staticmethod
    def __process_string_for_filter(original_string):
        # Ignore case & spaces
        return original_string.lower().replace(" ", "")
