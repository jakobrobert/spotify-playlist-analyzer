import sys


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    def get_size_in_bytes(self):
        own_size_in_bytes = sys.getsizeof(self)

        if not self.tracks:
            return own_size_in_bytes

        size_in_bytes_of_tracks = sum(track.get_size_in_bytes() for track in self.tracks)
        return own_size_in_bytes + size_in_bytes_of_tracks
