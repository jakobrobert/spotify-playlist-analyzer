import functools
import operator
import random

from flask import jsonify

from core.filter_params import FilterParams
from core.http_error import HttpError
from core.playlist_statistics.playlist_statistics import PlaylistStatistics
from core.track_filter import TrackFilter
from core.utils import Utils


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
                error =  HttpError.from_last_exception()
                return ApiUtils.create_error_response(error)

        return decorator

    @staticmethod
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
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
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
    def filter_tracks(tracks, request_args):
        filter_params = FilterParams.extract_filter_params_from_request_params(request_args)
        track_filter = TrackFilter(tracks, filter_params)
        return track_filter.filter_tracks()

    @staticmethod
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
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
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
    def sort_tracks(tracks, request_args):
        sort_by = request_args.get("sort_by") or "none"
        order = request_args.get("order") or "ascending"

        if sort_by == "none":
            return

        reverse = (order == "descending")
        tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)

    @staticmethod
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
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
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
    def get_attribute_distribution_items(attribute, tracks):
        statistics = PlaylistStatistics(tracks)

        if attribute == "duration_ms":
            return statistics.get_duration_distribution_items()
        if attribute == "release_year":
            return statistics.get_release_year_distribution_items()
        if attribute == "popularity":
            return statistics.get_popularity_distribution_items()
        if attribute == "super_genres":
            return statistics.get_super_genres_distribution_items()
        if attribute == "tempo":
            return statistics.get_tempo_distribution_items()
        if attribute == "key":
            return statistics.get_key_distribution_items()
        if attribute == "mode":
            return statistics.get_mode_distribution_items()
        if attribute == "key_signature":
            return statistics.get_key_signature_distribution_items()
        if attribute == "loudness":
            return statistics.get_loudness_distribution_items()
        if attribute == "danceability":
            return statistics.get_danceability_distribution_items()
        if attribute == "energy":
            return statistics.get_energy_distribution_items()
        if attribute == "valence":
            return statistics.get_valence_distribution_items()
        if attribute == "instrumentalness":
            return statistics.get_instrumentalness_distribution_items()
        if attribute == "acousticness":
            return statistics.get_acousticness_distribution_items()
        if attribute == "liveness":
            return statistics.get_liveness_distribution_items()
        if attribute == "speechiness":
            return statistics.get_speechiness_distribution_items()

        raise HttpError(400, "API Error", f"Invalid attribute: '{attribute}'")
