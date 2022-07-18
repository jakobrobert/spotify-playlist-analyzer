import requests

# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack
from spotify.spotify_playlist import SpotifyPlaylist
from http_error import HttpError


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    def get_playlist_by_id(self, playlist_id):
        if playlist_id is None:
            raise ValueError("playlist_id is None!")

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        access_token = self.__get_access_token()
        response_data = SpotifyClient.__send_get_request(url, access_token)

        if "error" in response_data:
            error = response_data["error"]
            status = error["status"]
            message = error["message"]

            raise HttpError(status, message)

        playlist = SpotifyPlaylist()
        # TODO CLEANUP get id from response for consistency
        playlist.id = playlist_id
        playlist.name = response_data["name"]
        playlist.tracks = SpotifyClient.__get_tracks_of_playlist(response_data, access_token)

        return playlist

    def __get_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        auth = (self.CLIENT_ID, self.CLIENT_SECRET)
        response = requests.post(url, data=data, auth=auth)
        response_data = response.json()

        return response_data["access_token"]

    @staticmethod
    def __send_get_request(url, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        return response.json()

    @staticmethod
    def __get_tracks_of_playlist(playlist_data, access_token):
        tracks = []

        track_items = SpotifyClient.__get_all_track_items_of_playlist(playlist_data, access_token)

        for track_item in track_items:
            track_data = track_item["track"]
            track = SpotifyClient.__create_spotify_track(track_data)
            tracks.append(track)

        SpotifyClient.__set_genres_of_tracks(tracks, access_token)
        SpotifyClient.__set_audio_features_of_tracks(tracks, access_token)

        return tracks

    @staticmethod
    def __get_all_track_items_of_playlist(playlist_data, access_token):
        tracks_data = playlist_data["tracks"]
        track_items = tracks_data["items"]
        next_url = tracks_data["next"]

        # Get remaining tracks, playlist_data only contains the first 100
        while next_url is not None:
            tracks_data = SpotifyClient.__send_get_request(next_url, access_token)
            new_track_items = tracks_data["items"]
            track_items.extend(new_track_items)
            next_url = tracks_data["next"]

        return track_items

    @staticmethod
    def __create_spotify_track(track_data):
        track = SpotifyTrack()

        track.id = track_data["id"]
        track.title = track_data["name"]
        track.artist_ids = SpotifyClient.__get_artist_ids_of_track(track_data)
        track.artists = SpotifyClient.__get_artists_of_track(track_data)
        track.duration_ms = track_data["duration_ms"]
        track.release_year = SpotifyClient.__get_release_year_of_track(track_data)

        return track

    @staticmethod
    def __get_artists_of_track(track):
        artist_names = []
        artists = track["artists"]

        for artist in artists:
            artist_names.append(artist["name"])

        return artist_names

    @staticmethod
    def __get_release_year_of_track(track):
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
    def __set_genres_of_tracks(tracks, access_token):
        all_artist_ids = []
        for track in tracks:
            all_artist_ids.extend(track.artist_ids)

        artist_id_to_genres = SpotifyClient.__get_artist_id_to_genres(all_artist_ids, access_token)

        for track in tracks:
            track.genres = SpotifyClient.__get_genres_of_artists(track.artist_ids, artist_id_to_genres)

    @staticmethod
    def __get_artist_id_to_genres(artist_ids, access_token):
        artist_id_to_genres = {}

        url = "https://api.spotify.com/v1/artists"
        max_ids_per_request = 50
        artist_id_chunks = SpotifyClient.__split_list_into_chunks(artist_ids, max_ids_per_request)

        for curr_artist_ids in artist_id_chunks:
            curr_artist_id_to_genres = SpotifyClient.__get_artist_id_to_genres_for_one_request(
                curr_artist_ids, url, access_token)
            artist_id_to_genres.update(curr_artist_id_to_genres)

        return artist_id_to_genres

    @staticmethod
    def __split_list_into_chunks(list_, chunk_size):
        chunks = []

        for start_index in range(0, len(list_), chunk_size):
            end_index = min(start_index + chunk_size, len(list_))
            chunk = list_[start_index:end_index]
            chunks.append(chunk)

        return chunks

    @staticmethod
    def __get_artist_id_to_genres_for_one_request(artist_ids, url, access_token):
        artist_id_to_genres = {}

        response_data = SpotifyClient.__send_get_request_with_ids(url, access_token, artist_ids)
        artists = response_data["artists"]

        for artist in artists:
            artist_id_to_genres[artist["id"]] = artist["genres"]

        return artist_id_to_genres

    @staticmethod
    def __send_get_request_with_ids(url, access_token, ids):
        headers = {"Authorization": f"Bearer {access_token}"}
        ids_string = ",".join(ids)
        params = {"ids": ids_string}
        response = requests.get(url, headers=headers, params=params)

        return response.json()

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
    def __set_audio_features_of_tracks(tracks, access_token):
        all_audio_features = SpotifyClient.__get_audio_features_of_tracks(tracks, access_token)

        assert len(all_audio_features) == len(tracks)

        for i in range(0, len(tracks)):
            audio_features = all_audio_features[i]
            track = tracks[i]
            track.tempo = audio_features["tempo"]
            track.key = audio_features["key"]
            track.mode = audio_features["mode"]
            key_string = track.get_key_string()
            mode_string = track.get_mode_string()
            track.key_signature = SpotifyClient.__get_key_signature_from_key_and_mode(key_string, mode_string)
            track.camelot = SpotifyClient.__get_camelot_from_key_and_mode(key_string, mode_string)
            track.loudness = audio_features["loudness"]

    @staticmethod
    def __get_audio_features_of_tracks(tracks, access_token):
        audio_features = []

        track_ids = []
        for track in tracks:
            track_ids.append(track.id)

        url = "https://api.spotify.com/v1/audio-features"
        max_ids_per_request = 100
        track_id_chunks = SpotifyClient.__split_list_into_chunks(track_ids, max_ids_per_request)

        for curr_track_ids in track_id_chunks:
            curr_audio_features = SpotifyClient.__get_audio_features_of_tracks_for_one_request(
                curr_track_ids, url, access_token)
            audio_features.extend(curr_audio_features)

        return audio_features

    @staticmethod
    def __get_audio_features_of_tracks_for_one_request(track_ids, url, access_token):
        response_data = SpotifyClient.__send_get_request_with_ids(url, access_token, track_ids)

        return response_data["audio_features"]

    # Key Signature & Camelot do not directly depend on SpotifyAPI but are derived from key & mode,
    # so might seem out of place here
    # -> Still determined here so SpotifyTrack immediately contains these attributes when created
    # -> Is important for sorting tracks

    @staticmethod
    def __get_key_signature_from_key_and_mode(key, mode):
        if (key == "C" and mode == "Major") or (key == "A" and mode == "Minor"):
            return "♮"
        if (key == "G" and mode == "Major") or (key == "E" and mode == "Minor"):
            return "1♯"
        if (key == "D" and mode == "Major") or (key == "B" and mode == "Minor"):
            return "2♯"
        if (key == "A" and mode == "Major") or (key == "F♯/G♭" and mode == "Minor"):
            return "3♯"
        if (key == "E" and mode == "Major") or (key == "C♯/D♭" and mode == "Minor"):
            return "4♯"
        if (key == "B" and mode == "Major") or (key == "G♯/A♭" and mode == "Minor"):
            return "5♯"
        if (key == "F♯/G♭" and mode == "Major") or (key == "D♯/E♭" and mode == "Minor"):
            return "6♯/6♭"
        if (key == "C♯/D♭" and mode == "Major") or (key == "A♯/B♭" and mode == "Minor"):
            return "5♭"
        if (key == "G♯/A♭" and mode == "Major") or (key == "F" and mode == "Minor"):
            return "4♭"
        if (key == "D♯/E♭" and mode == "Major") or (key == "C" and mode == "Minor"):
            return "3♭"
        if (key == "A♯/B♭" and mode == "Major") or (key == "G" and mode == "Minor"):
            return "2♭"
        if (key == "F" and mode == "Major") or (key == "D" and mode == "Minor"):
            return "1♭"

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
