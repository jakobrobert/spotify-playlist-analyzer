import random

from core.filter_params import FilterParams
from core.http_error import HttpError
from core.track_filter import TrackFilter
from core.utils import Utils


class ApiUtils:
    @staticmethod
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
    def filter_tracks(tracks, request_args):
        filter_params = FilterParams.extract_filter_params_from_request_params(request_args)
        track_filter = TrackFilter(tracks, filter_params)
        return track_filter.filter_tracks()

    @staticmethod
    @Utils.measure_execution_time(log_prefix="[API Helper] ")
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
