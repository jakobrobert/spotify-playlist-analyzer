from core.spotify.spotify_playlist_statistics import SpotifyPlaylistStatistics


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.statistics = SpotifyPlaylistStatistics()
        self.tracks = []

    # Cannot be static, else template code cannot access it
    def percentage_to_string(self, percentage):
        return f"{percentage:.1f}"

    def get_average_value_for_attribute(self, attribute):
        # TODONOW implement
        return 42
