from http_error import HttpError
from track_filter import TrackFilter


class FilterParams:
    @staticmethod
    def extract_filter_params_from_request_params(request_params):
        filter_by = request_params.get("filter_by") or None

        if filter_by is None:
            filter_params = {"filter_by": None}
            return filter_params

        if filter_by == "artists":
            return FilterParams.__extract_params_for_artists(request_params)

        if filter_by == "title":
            return FilterParams.__extract_params_for_title(request_params)

        if filter_by == "genres":
            return FilterParams.__extract_params_for_genres(request_params)

        if filter_by == "key":
            return FilterParams.__extract_params_for_key(request_params)

        if filter_by == "mode":
            return FilterParams.__extract_params_for_mode(request_params)

        if filter_by == "key_signature":
            return FilterParams.__extract_params_for_key_signature(request_params)

        if filter_by in TrackFilter.NUMBER_BASED_ATTRIBUTES:
            return FilterParams.__extract_params_for_number_based_attribute(request_params, filter_by)

        raise HttpError(400, "API Error", f"Invalid value for 'filter_by': '{filter_by}'")

    @staticmethod
    def __extract_params_for_artists(request_params):
        filter_params = {"filter_by": "artists"}

        artists_substring = request_params.get("artists_substring")
        if not artists_substring:
            raise FilterParams.__create_http_error_for_required_param("artists", "artists_substring")

        filter_params["artists_substring"] = artists_substring

        return filter_params

    @staticmethod
    def __extract_params_for_title(request_params):
        filter_params = {"filter_by": "title"}

        title_substring = request_params.get("title_substring")
        if not title_substring:
            raise FilterParams.__create_http_error_for_required_param("title", "title_substring")

        filter_params["title_substring"] = title_substring

        return filter_params

    @staticmethod
    def __extract_params_for_genres(request_params):
        filter_params = {"filter_by": "genres"}

        genres_substring = request_params.get("genres_substring")
        if not genres_substring:
            raise FilterParams.__create_http_error_for_required_param("genres", "genres_substring")

        filter_params["genres_substring"] = genres_substring
        return filter_params

    @staticmethod
    def __extract_params_for_key(request_params):
        filter_params = {"filter_by": "key"}

        expected_key = request_params.get("expected_key")
        if not expected_key:
            raise FilterParams.__create_http_error_for_required_param("key", "expected_key")

        filter_params["expected_key"] = expected_key
        return filter_params

    @staticmethod
    def __extract_params_for_mode(request_params):
        filter_params = {"filter_by": "mode"}

        expected_mode = request_params.get("expected_mode")
        if not expected_mode:
            raise FilterParams.__create_http_error_for_required_param("mode", "expected_mode")

        filter_params["expected_mode"] = expected_mode
        return filter_params

    @staticmethod
    def __extract_params_for_key_signature(request_params):
        filter_params = {"filter_by": "key_signature"}

        expected_key_signature = request_params.get("expected_key_signature")
        if not expected_key_signature:
            raise FilterParams.__create_http_error_for_required_param("key_signature", "expected_key_signature")

        filter_params["expected_key_signature"] = expected_key_signature
        return filter_params

    @staticmethod
    def __extract_params_for_number_based_attribute(request_params, attribute_name):
        filter_params = {"filter_by": attribute_name}

        min_value = FilterParams.__get_request_param_as_int_or_none(request_params, f"min_{attribute_name}")
        if min_value is None:
            raise FilterParams.__create_http_error_for_required_param(attribute_name, f"min_{attribute_name}")

        max_value = FilterParams.__get_request_param_as_int_or_none(request_params, f"max_{attribute_name}")
        if max_value is None:
            raise FilterParams.__create_http_error_for_required_param(attribute_name, f"max_{attribute_name}")

        filter_params[f"min_{attribute_name}"] = min_value
        filter_params[f"max_{attribute_name}"] = max_value

        return filter_params

    @staticmethod
    def __create_http_error_for_required_param(filter_by, required_param):
        message = f"'{required_param}' is required if 'filter_by' == '{filter_by}'"
        return HttpError(400, "API Error", message)

    @staticmethod
    def __get_request_param_as_int_or_none(request_params, name):
        value_string = request_params.get(name)

        if value_string:
            return int(value_string)

        return None
