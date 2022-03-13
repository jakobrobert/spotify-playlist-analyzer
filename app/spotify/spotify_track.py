class SpotifyTrack:
    def __init__(self):
        self.track_id = ""
        self.title = "n/a"
        self.artists = "n/a"   # TODO change to array of strings
        self.duration = "n/a"  # TODO change to TimeSpan
        self.year_of_release = -1
        self.artist_ids = []
        self.genres = "n/a"    # TODO change to array of strings
        self.tempo = -1.0
        self.key = "n/a"
        self.mode = "n/a"
        self.loudness = -1.0
