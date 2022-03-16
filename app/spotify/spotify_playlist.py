class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    def get_total_duration_ms(self):
        total_duration_ms = 0

        for track in self.tracks:
            total_duration_ms += track.duration_ms

        return total_duration_ms
