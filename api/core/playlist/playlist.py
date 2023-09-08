from core.playlist.track import Track


class Playlist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    @staticmethod
    def from_dict(playlist_dict):
        playlist = Playlist()

        playlist.id = playlist_dict["id"]
        playlist.name = playlist_dict["name"]
        tracks_dict = playlist_dict["tracks"]
        playlist.tracks = []

        for track_dict in tracks_dict:
            track = Track.from_dict(track_dict)
            playlist.tracks.append(track)

        return playlist
