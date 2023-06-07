from http_error import HttpError


class FilterParams:
    # TODONOW shorten method names, now that they are extracted into own class, scope is smaller so context is clear
    @staticmethod
    def extract_filter_params_from_request_params(request_params):
        filter_by = request_params.get("filter_by") or None

        if filter_by is None:
            filter_params = {"filter_by": None}
            return filter_params

        if filter_by == "artists":
            return FilterParams.__extract_filter_params_from_request_params_for_artists(request_params)

        if filter_by == "title":
            return FilterParams.__extract_filter_params_from_request_params_for_title(request_params)

        if filter_by == "genres":
            return FilterParams.__extract_filter_params_from_request_params_for_genres(request_params)

        if filter_by == "key":
            return FilterParams.__extract_filter_params_from_request_params_for_key(request_params)

        if filter_by == "mode":
            return FilterParams.__extract_filter_params_from_request_params_for_mode(request_params)

        if filter_by == "key_signature":
            return FilterParams.__extract_filter_params_from_request_params_for_key_signature(request_params)

        if filter_by == "release_year":
            return FilterParams.__extract_filter_params_from_request_params_for_release_year(request_params)

        if filter_by == "tempo":
            return FilterParams.__extract_filter_params_from_request_params_for_tempo(request_params)

        raise HttpError(400, "API Error", f"Invalid value for 'filter_by': '{filter_by}'")

    @staticmethod
    def __extract_filter_params_from_request_params_for_artists(request_params):
        filter_params = {"filter_by": "artists"}

        artists_substring = request_params.get("artists_substring")
        if not artists_substring:
            raise FilterParams.__create_http_error_for_filter_params("artists", "artists_substring")

        filter_params["artists_substring"] = artists_substring

        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_title(request_params):
        filter_params = {"filter_by": "title"}

        title_substring = request_params.get("title_substring")
        if not title_substring:
            raise FilterParams.__create_http_error_for_filter_params("title", "title_substring")

        filter_params["title_substring"] = title_substring

        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_genres(request_params):
        filter_params = {"filter_by": "genres"}

        genres_substring = request_params.get("genres_substring")
        if not genres_substring:
            raise FilterParams.__create_http_error_for_filter_params("genres", "genres_substring")

        filter_params["genres_substring"] = genres_substring
        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_key(request_params):
        filter_params = {"filter_by": "key"}

        expected_key = request_params.get("expected_key")
        if not expected_key:
            raise FilterParams.__create_http_error_for_filter_params("key", "expected_key")

        filter_params["expected_key"] = expected_key
        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_mode(request_params):
        filter_params = {"filter_by": "mode"}

        expected_mode = request_params.get("expected_mode")
        if not expected_mode:
            raise FilterParams.__create_http_error_for_filter_params("mode", "expected_mode")

        filter_params["expected_mode"] = expected_mode
        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_key_signature(request_params):
        filter_params = {"filter_by": "key_signature"}

        expected_key_signature = request_params.get("expected_key_signature")
        if not expected_key_signature:
            raise FilterParams.__create_http_error_for_filter_params("key_signature", "expected_key_signature")

        filter_params["expected_key_signature"] = expected_key_signature
        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_release_year(request_params):
        filter_params = {"filter_by": "release_year"}

        min_release_year = FilterParams.__get_request_param_as_int_or_none(request_params, "min_release_year")
        if min_release_year is None:
            raise FilterParams.__create_http_error_for_filter_params("release_year", "min_release_year")

        max_release_year = FilterParams.__get_request_param_as_int_or_none(request_params, "max_release_year")
        if max_release_year is None:
            raise FilterParams.__create_http_error_for_filter_params("release_year", "max_release_year")

        filter_params["min_release_year"] = min_release_year
        filter_params["max_release_year"] = max_release_year
        return filter_params

    @staticmethod
    def __extract_filter_params_from_request_params_for_tempo(request_params):
        filter_params = {"filter_by": "tempo"}

        min_tempo = FilterParams.__get_request_param_as_int_or_none(request_params, "min_tempo")
        if min_tempo is None:
            raise FilterParams.__create_http_error_for_filter_params("tempo", "min_tempo")

        max_tempo = FilterParams.__get_request_param_as_int_or_none(request_params, "max_tempo")
        if max_tempo is None:
            raise FilterParams.__create_http_error_for_filter_params("tempo", "max_tempo")

        filter_params["min_tempo"] = min_tempo
        filter_params["max_tempo"] = max_tempo
        return filter_params

    @staticmethod
    def __create_http_error_for_filter_params(filter_by, required_param):
        message = f"'{required_param}' is required if 'filter_by' == '{filter_by}'"
        return HttpError(400, "API Error", message)

    @staticmethod
    def __get_request_param_as_int_or_none(request_params, name):
        value_string = request_params.get(name)

        if value_string:
            return int(value_string)

        return None
