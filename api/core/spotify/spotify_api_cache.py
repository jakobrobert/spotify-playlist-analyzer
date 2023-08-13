from datetime import datetime


class SpotifyApiCache:
    class Item:
        def __init__(self, data):
            self.timestamp = datetime.now()
            self.data = data

    def __init__(self):
        self.__playlist_by_id_cache = {}

    def get_playlist_by_id(self, playlist_id):
        if playlist_id not in self.__playlist_by_id_cache:
            raise KeyError(f"No playlist found in cache for id: {playlist_id}")

        cache_item = self.__playlist_by_id_cache[playlist_id]
        # TODONOW Invalidate cache
        #   -> check if still up to date, compare timestamp to now. if up to date, return it
        #   -> else, return exception to indicate that out of date.
        return cache_item.data

    def update_playlist(self, playlist_id, playlist):
        self.__playlist_by_id_cache[playlist_id] = SpotifyApiCache.Item(playlist)
