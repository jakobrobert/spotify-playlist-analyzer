import copy
from datetime import datetime

CACHE_INVALIDATION_INTERVAL_IN_SECONDS = 5 * 60


class SpotifyApiCache:
    class Item:
        def __init__(self, data):
            self.timestamp = datetime.now()
            self.data = data

    def __init__(self):
        self.__playlist_by_id_cache = {}

    def get_playlist_by_id(self, playlist_id):
        if playlist_id not in self.__playlist_by_id_cache:
            return None

        cache_item = self.__playlist_by_id_cache[playlist_id]
        elapsed_time_since_last_cache_update = datetime.now() - cache_item.timestamp
        if elapsed_time_since_last_cache_update.total_seconds() >= CACHE_INVALIDATION_INTERVAL_IN_SECONDS:
            return None

        # Important to create copy of playlist.
        # -> Else, e.g. filtering playlist would cause that cache only contains filtered playlist.
        playlist = copy.deepcopy(cache_item.data)

        return playlist

    def update_playlist(self, playlist_id, playlist):
        # Important to create copy of playlist.
        # -> Else, e.g. filtering playlist would cause that cache only contains filtered playlist.
        playlist_copy = copy.deepcopy(playlist)
        self.__playlist_by_id_cache[playlist_id] = SpotifyApiCache.Item(playlist_copy)
