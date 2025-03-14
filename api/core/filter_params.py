from core.http_error import HttpError
from core.track_filter import TrackFilter
from core.utils import Utils


LOG_PREFIX = "FilterParams."


class FilterParams:
    # REMARK NO need to measure performance here, takes under 1 ms with hundreds of tracks
    # -> Not significant in comparison to requests in SpotifyApiClient which take several seconds in total
    @staticmethod
    def extract_filter_params_from_request_params(request_params):
        filter_by = request_params.get("filter_by") or None
        filter_params = {"filter_by": filter_by}

        if filter_by is None:
            return filter_params

        if filter_by == "artists":
            filter_params.update(FilterParams.__extract_params_for_artists(request_params))
            return filter_params

        if filter_by == "title":
            filter_params.update(FilterParams.__extract_params_for_title(request_params))
            return filter_params

        if filter_by == "added_by":
            filter_params.update(FilterParams.__extract_params_for_added_by(request_params))
            return filter_params

        if filter_by == "genres":
            filter_params.update(FilterParams.__extract_params_for_genres(request_params))
            return filter_params

        if filter_by == "super_genres":
            filter_params.update(FilterParams.__extract_params_for_super_genres(request_params))
            return filter_params

        if filter_by == "key":
            filter_params.update(FilterParams.__extract_params_for_key(request_params))
            return filter_params

        if filter_by == "mode":
            filter_params.update(FilterParams.__extract_params_for_mode(request_params))
            return filter_params

        if filter_by == "key_and_mode_pair":
            filter_params.update(FilterParams.__extract_params_for_key_and_mode_pair(request_params))
            return filter_params

        if filter_by == "key_signature":
            filter_params.update(FilterParams.__extract_params_for_key_signature(request_params))
            return filter_params

        if filter_by in TrackFilter.NUMERICAL_ATTRIBUTES:
            filter_params.update(FilterParams.__extract_params_for_numerical_attribute(request_params, filter_by))
            return filter_params

        raise HttpError(400, "API Error", f"FilterParams => Invalid value for 'filter_by': '{filter_by}'")

    @staticmethod
    def __extract_params_for_artists(request_params):
        filter_params = {}

        artists_substring = request_params.get("artists_substring")
        if not artists_substring:
            raise FilterParams.__create_http_error_for_required_param("artists", "artists_substring")

        filter_params["artists_substring"] = artists_substring
        return filter_params

    @staticmethod
    def __extract_params_for_title(request_params):
        filter_params = {}

        title_substring = request_params.get("title_substring")
        if not title_substring:
            raise FilterParams.__create_http_error_for_required_param("title", "title_substring")

        filter_params["title_substring"] = title_substring
        return filter_params

    @staticmethod
    def __extract_params_for_added_by(request_params):
        filter_params = {}

        added_by_substring = request_params.get("added_by_substring")
        if not added_by_substring:
            raise FilterParams.__create_http_error_for_required_param("added_by", "added_by_substring")

        filter_params["added_by_substring"] = added_by_substring
        return filter_params

    @staticmethod
    def __extract_params_for_genres(request_params):
        filter_params = {}

        genres_substring = request_params.get("genres_substring")
        if not genres_substring:
            raise FilterParams.__create_http_error_for_required_param("genres", "genres_substring")

        filter_params["genres_substring"] = genres_substring

        return filter_params

    @staticmethod
    def __extract_params_for_super_genres(request_params):
        filter_params = {}

        super_genres_substring = request_params.get("super_genres_substring")
        if not super_genres_substring:
            raise FilterParams.__create_http_error_for_required_param("super_genres", "super_genres_substring")

        filter_params["super_genres_substring"] = super_genres_substring

        return filter_params

    @staticmethod
    def __extract_params_for_key(request_params):
        filter_params = {}

        expected_key = Utils.get_request_arg_as_int_or_none(request_params, "expected_key")
        if expected_key is None:
            raise FilterParams.__create_http_error_for_required_param("key", "expected_key")

        filter_params["expected_key"] = expected_key
        return filter_params

    @staticmethod
    def __extract_params_for_mode(request_params):
        filter_params = {}

        expected_mode = Utils.get_request_arg_as_int_or_none(request_params, "expected_mode")
        if expected_mode is None:
            raise FilterParams.__create_http_error_for_required_param("mode", "expected_mode")

        filter_params["expected_mode"] = expected_mode
        return filter_params

    @staticmethod
    def __extract_params_for_key_and_mode_pair(request_params):
        filter_params = {}

        expected_key_and_mode_pair = Utils.get_request_arg_as_int_or_none(request_params, "expected_key_and_mode_pair")
        if expected_key_and_mode_pair is None:
            raise FilterParams.__create_http_error_for_required_param("key_and_mode_pair", "expected_key_and_mode_pair")

        filter_params["expected_key_and_mode_pair"] = expected_key_and_mode_pair
        return filter_params

    @staticmethod
    def __extract_params_for_key_signature(request_params):
        filter_params = {}

        expected_key_signature = request_params.get("expected_key_signature")
        if not expected_key_signature:
            raise FilterParams.__create_http_error_for_required_param("key_signature", "expected_key_signature")

        filter_params["expected_key_signature"] = expected_key_signature
        return filter_params

    @staticmethod
    def __extract_params_for_numerical_attribute(request_params, attribute_name):
        filter_params = {}

        min_value = Utils.get_request_arg_as_int_or_none(request_params, f"min_{attribute_name}")
        if min_value is None:
            raise FilterParams.__create_http_error_for_required_param(attribute_name, f"min_{attribute_name}")

        max_value = Utils.get_request_arg_as_int_or_none(request_params, f"max_{attribute_name}")
        if max_value is None:
            raise FilterParams.__create_http_error_for_required_param(attribute_name, f"max_{attribute_name}")

        filter_params[f"min_{attribute_name}"] = min_value
        filter_params[f"max_{attribute_name}"] = max_value
        return filter_params

    @staticmethod
    def __create_http_error_for_required_param(filter_by, required_param):
        message = f"'{required_param}' is required if 'filter_by' == '{filter_by}'"
        return HttpError(400, "API Error", message)
