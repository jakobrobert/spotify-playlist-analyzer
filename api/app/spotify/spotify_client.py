import requests
import json

# PyCharm shows errors for these imports locally, but it works this way with the server
# 'from spotify_track import SpotifyTrack' is shown as valid locally, but does not work with the server
from spotify.spotify_track import SpotifyTrack
from spotify.spotify_playlist import SpotifyPlaylist
from http_error import HttpError


class SpotifyClient:
    def __init__(self, client_id, client_secret, test_refresh_token, test_access_token, test_user_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.test_refresh_token = test_refresh_token
        self.test_access_token = test_access_token
        self.test_user_id = test_user_id

    def get_playlist_by_id(self, playlist_id):
        if playlist_id is None:
            raise HttpError(400, "playlist_id is None!")

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        access_token = self.__get_access_token_by_client_credentials()
        response_data = SpotifyClient.__send_get_request(url, access_token)

        playlist = SpotifyPlaylist()
        playlist.id = response_data["id"]
        playlist.name = response_data["name"]
        playlist.tracks = SpotifyClient.__get_tracks_of_playlist(response_data, access_token)

        return playlist

    # TODO add param track_ids
    def create_playlist(self, playlist_name):
        if not playlist_name:
            raise HttpError(400, "playlist_name is invalid!")

        # TODO Very strange bug! When using access token directly, creates playlist successfully.
        #   When trying to get access token by refresh token, returns error:
        #   status code 401 with message "invalid_client"
        #   But checked values in ini, they are consistent, both refresh & access token are from same authorization request
        #   And logged the values and compared, they also fit
        print(f"create_playlist => test_access_token: {self.test_access_token}")
        print(f"create_playlist => test_refresh_token: {self.test_refresh_token}")

        access_token = self.test_access_token
        #access_token = self.__get_access_token_by_refresh_token()
        print(f"create_playlist => access_token: {self.test_access_token}")

        playlist_id = self.__create_empty_playlist(playlist_name, self.test_user_id, access_token)

        # TODO add tracks to playlist, can just convert track_ids to spotify uris.
        # TODO see here: https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist

        return playlist_id

    def get_track_by_id(self, track_id):
        if track_id is None:
            raise HttpError(400, "track_id is None!")

        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        access_token = self.__get_access_token_by_client_credentials()
        track_data = SpotifyClient.__send_get_request(url, access_token)

        track = SpotifyClient.__create_spotify_track(track_data)
        tracks = [track]
        SpotifyClient.__set_genres_of_tracks(tracks, access_token)
        SpotifyClient.__set_audio_features_of_tracks(tracks, access_token)

        return track

    def search_tracks(self, query):
        if query is None:
            raise HttpError(400, "query is None!")

        url = f"https://api.spotify.com/v1/search"
        access_token = self.__get_access_token_by_client_credentials()
        params = {
            "q": query,
            "type": "track",
            "limit": 50
        }

        response_data = SpotifyClient.__send_get_request(url, access_token, params)
        tracks_data = response_data["tracks"]
        track_items = tracks_data["items"]

        tracks = []

        for track_item in track_items:
            track = SpotifyClient.__create_spotify_track(track_item)
            tracks.append(track)

        SpotifyClient.__set_genres_of_tracks(tracks, access_token)
        SpotifyClient.__set_audio_features_of_tracks(tracks, access_token)

        return tracks

    def __get_access_token_by_client_credentials(self):
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        auth = (self.client_id, self.client_secret)
        response = requests.post(url, data=data, auth=auth)
        response_data = response.json()

        error = SpotifyClient.__create_http_error_from_response_data(response_data)
        if error:
            raise error

        return response_data["access_token"]

    def __get_access_token_by_refresh_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": f"Basic {self.client_id}:{self.client_secret}",
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "refresh_token", "refresh_token": self.test_refresh_token}
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        # TODO returns error with message "invalid_client"
        if "error" in response_data:
            error_title = "Spotify API Error: Failed to get access token by refresh token"
            # Note that this is different to other endpoints, so cannot use __create_http_error_from_response_data here
            error_message = response_data["error"]
            raise HttpError(response.status_code, error_title, error_message)

        return response_data["access_token"]

    @staticmethod
    def __send_get_request(url, access_token, params=None):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        error = SpotifyClient.__create_http_error_from_response_data(response_data)
        if error:
            raise error

        return response_data

    @staticmethod
    def __create_http_error_from_response_data(response_data):
        if "error" not in response_data:
            return None

        error = response_data["error"]
        status_code = error["status"]
        message = error["message"]
        title = "Spotify API Error"

        return HttpError(status_code, title, message)

    @staticmethod
    def __send_get_request_with_ids(url, access_token, ids):
        ids_string = ",".join(ids)
        params = {"ids": ids_string}

        return SpotifyClient.__send_get_request(url, access_token, params)

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
    def __create_empty_playlist(playlist_name, user_id, access_token):
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        data = {
            "name": playlist_name,
            "public": True
        }
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data_as_json = json.dumps(data)
        response = requests.post(url, headers=headers, data=data_as_json)

        try:
            response_data = response.json()
        except Exception:
            raise HttpError(status_code=response.status_code, title="Spotify API Error", message=response.text)

        error = SpotifyClient.__create_http_error_from_response_data(response_data)
        if error:
            raise error

        return response_data["id"]

    @staticmethod
    def __create_spotify_track(track_data):
        track = SpotifyTrack()

        track.id = track_data["id"]
        track.title = track_data["name"]
        track.artist_ids = SpotifyClient.__get_artist_ids_of_track(track_data)
        track.artists = SpotifyClient.__get_artists_of_track(track_data)
        track.duration_ms = track_data["duration_ms"]
        track.release_year = SpotifyClient.__get_release_year_of_track(track_data)
        track.popularity = track_data["popularity"]

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
        audio_features_by_track = SpotifyClient.__get_audio_features_of_tracks(tracks, access_token)

        assert len(audio_features_by_track) == len(tracks)

        for i in range(0, len(tracks)):
            tracks[i].update_attributes_by_audio_features(audio_features_by_track[i])

    @staticmethod
    def __get_audio_features_of_tracks(tracks, access_token):
        audio_features_by_track = []

        track_ids = []
        for track in tracks:
            track_ids.append(track.id)

        url = "https://api.spotify.com/v1/audio-features"
        max_ids_per_request = 100
        track_id_chunks = SpotifyClient.__split_list_into_chunks(track_ids, max_ids_per_request)

        for track_ids_of_chunk in track_id_chunks:
            response_data = SpotifyClient.__send_get_request_with_ids(url, access_token, track_ids_of_chunk)
            audio_features_by_track.extend(response_data["audio_features"])

        return audio_features_by_track
