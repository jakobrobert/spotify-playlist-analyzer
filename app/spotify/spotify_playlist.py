# PyCharm shows errors for this import locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack


class SpotifyPlaylist:
    # TODO duplicated with SpotifyClient, but need to do this way because circular import when importing SpotifyClient
    KEY_NAMES = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]

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

        for key_name in SpotifyPlaylist.KEY_NAMES:
            key_to_count[key_name] = 0

        key_to_count["n/a"] = 0

        for track in self.tracks:
            key_to_count[track.key] += 1

        key_to_percentage = {}

        for key, count in key_to_count.items():
            proportion = count / len(self.tracks)
            key_to_percentage[key] = proportion * 100.0

        return key_to_percentage

    def get_mode_to_percentage(self):
        mode_to_count = {
            "Major": 0,
            "Minor": 0,
            "n/a": 0
        }

        for track in self.tracks:
            mode_to_count[track.mode] += 1

        mode_to_percentage = {}

        # TODO clean up: duplicated code with get_key_to_percentage()
        for mode, count in mode_to_count.items():
            proportion = count / len(self.tracks)
            mode_to_percentage[mode] = proportion * 100.0

        return mode_to_percentage
