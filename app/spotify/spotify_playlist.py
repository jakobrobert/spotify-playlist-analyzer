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

    def get_total_duration_string(self):
        total_milliseconds = self.get_total_duration_ms()
        total_seconds = total_milliseconds // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60

        return f"{total_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"

    def get_average_duration_ms(self):
        total_duration_ms = self.get_total_duration_ms()
        return total_duration_ms / len(self.tracks)

    def get_average_duration_string(self):
        average_duration_ms = int(self.get_average_duration_ms())
        # TODO clean up: duplicated code with SpotifyTrack
        total_seconds = average_duration_ms // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"
