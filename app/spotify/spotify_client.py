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
        # TODO CLEANUP extract method?
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        access_token = self.__get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        playlist_data = response.json()

        playlist = SpotifyPlaylist()
        playlist.id = playlist_id
        playlist.name = playlist_data["name"]
        playlist.tracks = SpotifyClient.__get_tracks_of_playlist(playlist_data, access_token)

        return playlist

    def __get_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        auth = (self.CLIENT_ID, self.CLIENT_SECRET)
        response = requests.post(url, data=data, auth=auth)
        response_data = response.json()

        return response_data["access_token"]

    @staticmethod
    def __get_tracks_of_playlist(playlist_data, access_token):
        tracks = []

        tracks_data = playlist_data["tracks"]
        track_items = tracks_data["items"]
        next_url = tracks_data["next"]

        # Get remaining tracks, playlist_data only contains the first 100
        while next_url is not None:
            # TODO CLEANUP these three lines are duplicated for all GET requests
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(next_url, headers=headers)
            tracks_data = response.json()

            new_track_items = tracks_data["items"]
            track_items.extend(new_track_items)
            next_url = tracks_data["next"]

        track_ids = []
        artist_ids_per_track = []
        all_artist_ids = []

        for track_item in track_items:
            track_data = track_item["track"]

            track = SpotifyTrack()
            track.title = track_data["name"]
            track.artists = SpotifyClient.__get_artists_of_track(track_data)
            track.duration_ms = track_data["duration_ms"]
            track.year_of_release = SpotifyClient.__get_year_of_release_of_track(track_data)
            tracks.append(track)

            track_ids.append(track_data["id"])

            artist_ids = SpotifyClient.__get_artist_ids_of_track(track_data)
            artist_ids_per_track.append(artist_ids)
            all_artist_ids.extend(artist_ids)

        SpotifyClient.__set_genres_of_tracks(tracks, all_artist_ids, artist_ids_per_track, access_token)
        SpotifyClient.__set_audio_features_of_tracks(tracks, track_ids, access_token)

        return tracks

    @staticmethod
    def __get_artists_of_track(track):
        artist_names = []
        artists = track["artists"]

        for artist in artists:
            artist_names.append(artist["name"])

        return artist_names

    @staticmethod
    def __get_year_of_release_of_track(track):
        album = track["album"]
        release_date = album["release_date"]

        year_end_index = release_date.find("-")

        if year_end_index == -1:
            return int(release_date)

        return int(release_date[:year_end_index])

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
        all_audio_features = SpotifyClient.__get_audio_features_of_tracks(track_ids, access_token)

        assert len(all_audio_features) == len(tracks)

        for i in range(0, len(tracks)):
            audio_features = all_audio_features[i]
            track = tracks[i]
            track.tempo = audio_features["tempo"]
            track.key = SpotifyClient.__get_key_from_audio_features(audio_features)
            track.mode = SpotifyClient.__get_mode_from_audio_features(audio_features)
            track.camelot = SpotifyClient.__get_camelot_from_key_and_mode(track.key, track.mode)
            track.loudness = audio_features["loudness"]

    @staticmethod
    def __get_audio_features_of_tracks(track_ids, access_token):
        audio_features = []

        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {access_token}"}

        # TODO CLEANUP partly duplicated code with __get_artist_id_to_genres
        max_ids_per_request = 100
        for i in range(0, len(track_ids), max_ids_per_request):
            end_index = min(i + max_ids_per_request, len(track_ids))
            curr_track_ids = track_ids[i:end_index]
            curr_audio_features = SpotifyClient.__get_audio_features_of_tracks_for_one_request(
                curr_track_ids, url, headers)
            audio_features.extend(curr_audio_features)

        return audio_features

    @staticmethod
    def __get_audio_features_of_tracks_for_one_request(track_ids, url, headers):
        # TODO CLEANUP partly duplicated code with __get_artist_id_to_genres_for_one_request
        track_ids_string = ",".join(track_ids)
        params = {"ids": track_ids_string}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        return response_data["audio_features"]

    @staticmethod
    def __get_key_from_audio_features(audio_features):
        # TODO inline method
        return audio_features["key"]
        """
        key = audio_features["key"]

        if key == -1:
            return "n/a"

        return SpotifyClient.KEY_NAMES[key]
        """

    @staticmethod
    def __get_mode_from_audio_features(audio_features):
        mode = audio_features["mode"]

        if mode == 0:
            return "Minor"

        if mode == 1:
            return "Major"

        return "n/a"

    @staticmethod
    def __get_camelot_from_key_and_mode(key, mode):
        if key == "G♯/A♭" and mode == "Minor":
            return "01A"
        if key == "B" and mode == "Major":
            return "01B"
        if key == "D♯/E♭" and mode == "Minor":
            return "02A"
        if key == "F♯/G♭" and mode == "Major":
            return "02B"
        if key == "A♯/B♭" and mode == "Minor":
            return "03A"
        if key == "C♯/D♭" and mode == "Major":
            return "03B"
        if key == "F" and mode == "Minor":
            return "04A"
        if key == "G♯/A♭" and mode == "Major":
            return "04B"
        if key == "C" and mode == "Minor":
            return "05A"
        if key == "D♯/E♭" and mode == "Major":
            return "05B"
        if key == "G" and mode == "Minor":
            return "06A"
        if key == "A♯/B♭" and mode == "Major":
            return "06B"
        if key == "D" and mode == "Minor":
            return "07A"
        if key == "F" and mode == "Major":
            return "07B"
        if key == "A" and mode == "Minor":
            return "08A"
        if key == "C" and mode == "Major":
            return "08B"
        if key == "E" and mode == "Minor":
            return "09A"
        if key == "G" and mode == "Major":
            return "09B"
        if key == "B" and mode == "Minor":
            return "10A"
        if key == "D" and mode == "Major":
            return "10B"
        if key == "F♯/G♭" and mode == "Minor":
            return "11A"
        if key == "A" and mode == "Major":
            return "11B"
        if key == "C♯/D♭" and mode == "Minor":
            return "12A"
        if key == "E" and mode == "Major":
            return "12B"

        return "n/a"
