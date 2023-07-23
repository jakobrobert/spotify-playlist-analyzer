from core.filter_params import FilterParams
from core.track_filter import TrackFilter
from core.utils import Utils


class ApiUtils:
    @staticmethod
    @Utils.measure_execution_time(log_prefix="ApiUtils.")
    def filter_tracks(tracks, request_args):
        filter_params = FilterParams.extract_filter_params_from_request_params(request_args)
        track_filter = TrackFilter(tracks, filter_params)
        return track_filter.filter_tracks()
