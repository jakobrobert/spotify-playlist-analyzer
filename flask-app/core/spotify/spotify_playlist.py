from core.spotify.spotify_track import SpotifyTrack


class SpotifyPlaylist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    # Cannot be static, else template code cannot access it
    def percentage_to_string(self, percentage):
        return f"{percentage:.1f}"
