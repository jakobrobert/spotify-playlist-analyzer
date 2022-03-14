import requests

# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack
from spotify.spotify_playlist import SpotifyPlaylist


class SpotifyClient:
    KEY_NAMES = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]

    def __init__(self, client_id, client_secret):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    def get_playlist_by_id(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        access_token = self.__get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        playlist_data = response.json()

        playlist = SpotifyPlaylist()
        playlist.name = playlist_data["name"]

        # TODO extract method get_tracks_of_playlist(response_data)
        track_items = playlist_data["tracks"]["items"]

        tracks = []
        all_artist_ids = []
        artist_ids_per_track = []
        track_ids = []

        for track_item in track_items:
            track_data = track_item["track"]

            track = SpotifyTrack()
            track.title = track_data["name"]
            track.artists = SpotifyClient.__get_artists_of_track(track_data)
            track.duration = SpotifyClient.__get_duration_of_track(track_data)
            track.year_of_release = SpotifyClient.__get_year_of_release_of_track(track_data)
            tracks.append(track)

            track_ids.append(track_data["id"])

            artist_ids = SpotifyClient.__get_artist_ids_of_track(track_data)
            artist_ids_per_track.append(artist_ids)
            all_artist_ids.extend(artist_ids)

        SpotifyClient.__set_genres_of_tracks(tracks, all_artist_ids, artist_ids_per_track, access_token)
        SpotifyClient.__set_audio_features_of_tracks(tracks, track_ids, access_token)

        playlist.tracks = tracks

        return playlist

    def __get_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        auth = (self.CLIENT_ID, self.CLIENT_SECRET)
        response = requests.post(url, data=data, auth=auth)
        response_data = response.json()

        return response_data["access_token"]

    @staticmethod
    def __get_artists_of_track(track):
        artist_names = []
        artists = track["artists"]

        for artist in artists:
            artist_names.append(artist["name"])

        return artist_names

    @staticmethod
    def __get_duration_of_track(track):
        milliseconds = track["duration_ms"]
        total_seconds = milliseconds // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"

    @staticmethod
    def __get_year_of_release_of_track(track):
        album = track["album"]
        release_date = album["release_date"]

        year_end_index = release_date.find("-")

        if year_end_index == -1:
            return release_date

        return release_date[:year_end_index]

    @staticmethod
    def __get_artist_ids_of_track(track):
        artist_ids = []
        artists = track["artists"]

        for artist in artists:
            artist_id = artist["id"]
            artist_ids.append(artist_id)

        return artist_ids

    @staticmethod
    def __set_genres_of_tracks(tracks, all_artist_ids, artist_ids_per_track, access_token):
        artist_id_to_genres = SpotifyClient.__get_artist_id_to_genres(all_artist_ids, access_token)

        for track_index in range(0, len(tracks)):
            artist_ids = artist_ids_per_track[track_index]
            track = tracks[track_index]
            track.genres = SpotifyClient.__get_genres_of_artists(artist_ids, artist_id_to_genres)

    @staticmethod
    def __get_artist_id_to_genres(artist_ids, access_token):
        artist_id_to_genres = {}

        url = "https://api.spotify.com/v1/artists"
        headers = {"Authorization": f"Bearer {access_token}"}

        max_ids_per_request = 50
        for i in range(0, len(artist_ids), max_ids_per_request):
            end_index = min(i + max_ids_per_request, len(artist_ids))
            curr_artist_ids = artist_ids[i:end_index]
            SpotifyClient.__get_artist_id_to_genres_for_one_request(curr_artist_ids, url, headers, artist_id_to_genres)

        return artist_id_to_genres

    @staticmethod
    def __get_artist_id_to_genres_for_one_request(artist_ids, url, headers, artist_id_to_genres):
        artist_ids_string = ",".join(artist_ids)
        params = {"ids": artist_ids_string}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        artists = response_data["artists"]
        for artist in artists:
            artist_id_to_genres[artist["id"]] = artist["genres"]

    @staticmethod
    def __get_genres_of_artists(artist_ids, artist_id_to_genres):
        genres = []

        for artist_id in artist_ids:
            genres_of_artist = artist_id_to_genres[artist_id]
            for genre in genres_of_artist:
                if genre not in genres:
                    genres.append(genre)

        return genres

    @staticmethod
    def __set_audio_features_of_tracks(tracks, track_ids, access_token):
        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {access_token}"}
        # TODO #5 once more than 100 songs are supported, separate into several requests as done for genres
        track_ids_string = ','.join(track_ids)
        params = {"ids": track_ids_string}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        all_audio_features = response_data["audio_features"]

        assert len(all_audio_features) == len(tracks)

        for i in range(0, len(tracks)):
            audio_features = all_audio_features[i]
            track = tracks[i]
            track.tempo = audio_features["tempo"]
            track.key = SpotifyClient.__get_key_from_audio_features(audio_features)
            track.mode = SpotifyClient.__get_mode_from_audio_features(audio_features)
            track.loudness = audio_features["loudness"]

    @staticmethod
    def __get_key_from_audio_features(audio_features):
        key = audio_features["key"]

        if key == -1:
            return "n/a"

        return SpotifyClient.KEY_NAMES[key]

    @staticmethod
    def __get_mode_from_audio_features(audio_features):
        mode = audio_features["mode"]

        if mode == 0:
            return "Minor"

        if mode == 1:
            return "Major"

        return "n/a"
