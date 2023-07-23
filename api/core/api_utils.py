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
        }
