from core.playlist.track import Track


class Playlist:
    def __init__(self):
        self.id = "n/a"
        self.name = "n/a"
        self.tracks = []

    def to_dict(self):
        # Need to explicitly copy the dict, else changing the dict would change the original object
        playlist_dict = dict(self.__dict__)

        # Need to convert tracks to dict manually, playlist.__dict__ does not work recursively
        playlist_dict["tracks"] = []
        for track in self.tracks:
            # Explicitly copy dict for consistency and robustness
            track_dict = dict(track.__dict__)
            playlist_dict["tracks"].append(track_dict)

        return playlist_dict

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
