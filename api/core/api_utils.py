import functools
import operator
import random

from flask import jsonify

from core.analysis.attribute_distribution import AttributeDistribution
from core.filter_params import FilterParams
from core.http_error import HttpError
from core.analysis.playlist_statistics import PlaylistStatistics
from core.track_filter import TrackFilter
from core.utils import Utils


LOG_PREFIX = "ApiUtils."


# REMARK NO need to measure performance for helper methods in these class currently.
# -> Currently all take a few ms or even less than a ms even with hundreds of tracks
# -> Not significant in comparison to requests in SpotifyApiClient which take several seconds in total
class ApiUtils:
    @staticmethod
    def handle_exceptions(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HttpError as error:
                return ApiUtils.create_error_response(error)
            except Exception:
                error = HttpError.from_last_exception()
                return ApiUtils.create_error_response(error)

        return decorator

    @staticmethod
    def create_error_response(error):
        # Need to convert traceback_items manually, __dict__ is not supported
        traceback_items_converted = []

        for traceback_item in error.traceback_items:
            traceback_item_converted = []

            for traceback_item_attribute in traceback_item:
                traceback_item_converted.append(str(traceback_item_attribute))

            traceback_items_converted.append(traceback_item_converted)

        response_data = {
            "error": {
                "status_code": error.status_code,
                "title": error.title,
                "message": error.message,
                "traceback_items": traceback_items_converted
            }
        }

        response = jsonify(response_data)
        return response, error.status_code

    @staticmethod
    def filter_tracks(tracks, request_args):
        filter_params = FilterParams.extract_filter_params_from_request_params(request_args)
        track_filter = TrackFilter(tracks, filter_params)
        return track_filter.filter_tracks()

    @staticmethod
    def pick_random_tracks(tracks, request_args):
        pick_random_tracks_enabled = request_args.get("pick_random_tracks_enabled") == "on"
        if not pick_random_tracks_enabled:
            return

        pick_random_tracks_count = Utils.get_request_arg_as_int_or_none(request_args, "pick_random_tracks_count")
        if pick_random_tracks_count is None:
            raise HttpError(400, "API Error", "Missing request arg 'pick_random_tracks_count'")

        if pick_random_tracks_count < 0:
            raise HttpError(
                400, "API Error",
                "Invalid value for request arg 'pick_random_tracks_count' -> must be > 0"
            )

        if pick_random_tracks_count >= len(tracks):
            return

        random.shuffle(tracks)
        del tracks[pick_random_tracks_count:]

    @staticmethod
    def sort_tracks(tracks, request_args):
        sort_by = request_args.get("sort_by") or "none"
        order = request_args.get("order") or "ascending"

        if sort_by == "none":
            return

        reverse = (order == "descending")
        tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)

    @staticmethod
    def create_playlist_statistics_dict(tracks):
        statistics = PlaylistStatistics(tracks)

        return {
            "total_duration_ms": statistics.get_total_duration_ms(),
            "average_duration_ms": statistics.get_average_duration_ms(),
            "average_release_year": statistics.get_average_release_year(),
            "average_popularity": statistics.get_average_popularity(),
            "average_tempo": statistics.get_average_tempo(),
            "average_danceability": statistics.get_average_danceability(),
            "average_energy": statistics.get_average_energy(),
            "average_valence": statistics.get_average_valence(),
            "average_instrumentalness": statistics.get_average_instrumentalness(),
            "average_acousticness": statistics.get_average_acousticness(),
            "average_liveness": statistics.get_average_liveness(),
            "average_speechiness": statistics.get_average_speechiness(),
        }

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def get_attribute_distribution_items(attribute, tracks):
        attribute_distribution = AttributeDistribution(tracks)

        function_by_attribute_dict = {
            "duration_ms": attribute_distribution.get_duration_distribution_items,
            "release_year": attribute_distribution.get_release_year_distribution_items,
            "popularity": attribute_distribution.get_popularity_distribution_items,
            "super_genres": attribute_distribution.get_super_genres_distribution_items,
            "tempo": attribute_distribution.get_tempo_distribution_items,
            "key": attribute_distribution.get_key_distribution_items,
            "mode": attribute_distribution.get_mode_distribution_items,
            "key_signature": attribute_distribution.get_key_signature_distribution_items,
            "loudness": attribute_distribution.get_loudness_distribution_items,
            "danceability": attribute_distribution.get_danceability_distribution_items,
            "energy": attribute_distribution.get_energy_distribution_items,
            "valence": attribute_distribution.get_valence_distribution_items,
            "instrumentalness": attribute_distribution.get_instrumentalness_distribution_items,
            "acousticness": attribute_distribution.get_acousticness_distribution_items,
            "liveness": attribute_distribution.get_liveness_distribution_items,
            "speechiness": attribute_distribution.get_speechiness_distribution_items
        }

        if attribute in function_by_attribute_dict:
            return function_by_attribute_dict[attribute]()

        raise HttpError(400, "API Error", f"Invalid attribute: '{attribute}'")
