# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack


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
        return self.get_total_duration_ms() / len(self.tracks)

    def get_average_duration_string(self):
        average_duration_ms = int(self.get_average_duration_ms())

        return SpotifyTrack.get_duration_string_helper(average_duration_ms)

    def get_average_tempo(self):
        total_tempo = 0.0

        for track in self.tracks:
            total_tempo += track.tempo

        return total_tempo / len(self.tracks)

    def get_average_tempo_string(self):
        average_tempo = self.get_average_tempo()

        return f"{average_tempo:.1f}"

    def get_key_to_percentage(self):
        key_to_count = {}

        for track in self.tracks:
            if track.key in key_to_count:
                key_to_count[track.key] += 1
            else:
                key_to_count[track.key] = 1

        key_to_percentage = {}

        for key in key_to_count: # TODO clean up: use key, percentage in ...items()
            proportion = key_to_count[key] / len(self.tracks)
            key_to_percentage[key] = proportion * 100.0

        # TODO sort, maybe can fix by adding all keys in beginning

        return key_to_percentage
