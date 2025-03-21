import configparser
from math import ceil

from core.http_error import HttpError
from core.playlist.playlist import Playlist
from core.playlist.track import Track
from core.spotify_api.spotify_api_cache import SpotifyApiCache
from core.spotify_api.spotify_api_utils import SpotifyApiUtils
from core.utils import Utils

LOG_PREFIX = "SpotifyApiClient."


class SpotifyApiClient:
    def __init__(self, test_user_id, authorization):
        self.authorization = authorization
        self.cache = SpotifyApiCache()
        self.test_user_id = test_user_id

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_playlist_by_id(self, playlist_id):
        if not playlist_id:
            raise HttpError(400, title="API: get_playlist_by_id failed", message="'playlist_id' is None or empty")

        playlist_from_cache = self.cache.get_playlist_by_id(playlist_id)
        if playlist_from_cache:
            print(f"SpotifyApiClient.get_playlist_by_id => Got playlist from cache")
            return playlist_from_cache

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        access_token = self.authorization.get_access_token_by_client_credentials()
        response_data = SpotifyApiUtils.send_get_request(url, access_token)

        playlist = Playlist()
        playlist.id = response_data["id"]
        playlist.name = response_data["name"]
        playlist.tracks = SpotifyApiClient.__get_tracks_of_playlist(response_data, access_token)

        # TODONOW remove
        print(f"tracks: {len(playlist.tracks)}")

        self.cache.update_playlist(playlist_id, playlist)
        print(f"{LOG_PREFIX}.get_playlist_by_id => Updated playlist in cache")

        return playlist

    @Utils.measure_execution_time(LOG_PREFIX)
    def create_playlist(self, playlist_name, track_ids):
        if not playlist_name:
            raise HttpError(400, title="API: create_playlist failed", message="'playlist_name' is None or empty")

        if not track_ids:
            raise HttpError(400, title="API: create_playlist failed", message="'track_ids' is None or empty")

        # TODOLATER #171 Fix: Get access token by refresh token fails
        # As current workaround, read access token from ini file.
        # access token is written to ini file by authorize endpoint which can easily be called by Browser, see

        # Important to read it here from file
        # NOT before initialization of SpotifyApiClient, so it is always up-to-date
        test_access_token_config = configparser.ConfigParser()
        test_access_token_config.read("./test_access_token.ini")
        test_access_token = test_access_token_config["SPOTIFY"]["TEST_ACCESS_TOKEN"]
        print(f"create_playlist => test_access_token: {test_access_token}")

        playlist_id = SpotifyApiClient.__create_empty_playlist(playlist_name, self.test_user_id, test_access_token)
        SpotifyApiClient.__add_tracks_to_playlist(playlist_id, track_ids, test_access_token)

        return playlist_id

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_track_by_id(self, track_id):
        if track_id is None:
            raise HttpError(400, "track_id is None!")

        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        access_token = self.authorization.get_access_token_by_client_credentials()
        track_data = SpotifyApiUtils.send_get_request(url, access_token)

        track = SpotifyApiClient.__convert_dict_to_track(track_data)
        tracks = [track]
        SpotifyApiClient.__update_genres_of_tracks(tracks, access_token)
        SpotifyApiClient.__update_audio_features_of_tracks(tracks, access_token)

        return track

    @Utils.measure_execution_time(LOG_PREFIX)
    def search_tracks(self, query):
        if query is None:
            raise HttpError(400, "query is None!")

        url = f"https://api.spotify.com/v1/search"
        access_token = self.authorization.get_access_token_by_client_credentials()
        params = {
            "q": query,
            "type": "track",
            "limit": 50
        }

        response_data = SpotifyApiUtils.send_get_request(url, access_token, params)
        tracks_data = response_data["tracks"]
        track_items = tracks_data["items"]

        tracks = []

        for track_item in track_items:
            track = SpotifyApiClient.__convert_dict_to_track(track_item)
            tracks.append(track)

        SpotifyApiClient.__update_genres_of_tracks(tracks, access_token)
        SpotifyApiClient.__update_audio_features_of_tracks(tracks, access_token)

        return tracks

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_tracks_of_playlist(playlist_data, access_token):
        tracks = []

        track_items = SpotifyApiClient.__get_all_track_items_of_playlist(playlist_data, access_token)

        for track_item in track_items:
            added_by_user_id = track_item["added_by"]["id"]
            track_data = track_item["track"]
            track = SpotifyApiClient.__convert_dict_to_track(track_data)
            track.added_by_user_id = added_by_user_id
            tracks.append(track)

        SpotifyApiClient.__update_added_by_of_tracks(tracks, access_token)
        SpotifyApiClient.__update_genres_of_tracks(tracks, access_token)
        SpotifyApiClient.__update_audio_features_of_tracks(tracks, access_token)

        return tracks

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_all_track_items_of_playlist(playlist_data, access_token):
        tracks_data = playlist_data["tracks"]

        total_track_count = tracks_data["total"]
        expected_request_count = ceil(total_track_count / 100)

        print(f"SpotifyApiClient.__get_all_track_items_of_playlist => "
              f"total_track_count: {total_track_count}, expected_request_count: {expected_request_count}")

        all_track_items = []

        curr_track_items = tracks_data["items"]
        all_track_items.extend(curr_track_items)
        next_url = tracks_data["next"]

        # Get remaining tracks, playlist_data only contains the first 100
        while next_url is not None:
            curr_track_items, next_url = SpotifyApiClient.__get_track_items_for_one_request(next_url, access_token)
            all_track_items.extend(curr_track_items)

        return all_track_items

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_track_items_for_one_request(next_url, access_token):
        tracks_data = SpotifyApiUtils.send_get_request(next_url, access_token)
        track_items = tracks_data["items"]
        next_url = tracks_data["next"]

        return track_items, next_url

    @staticmethod
    def __convert_dict_to_track(track_dict):
        track = Track()

        track.id = track_dict["id"]
        track.title = track_dict["name"]
        track.artist_ids = SpotifyApiClient.__get_artist_ids_of_track(track_dict)
        track.artists = SpotifyApiClient.__get_artists_of_track(track_dict)
        track.duration_ms = track_dict["duration_ms"]
        track.release_year = SpotifyApiClient.__get_release_year_of_track(track_dict)
        track.popularity = track_dict["popularity"]

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
    @Utils.measure_execution_time(LOG_PREFIX)
    def __update_added_by_of_tracks(tracks, access_token):
        all_added_by_user_ids = []
        for track in tracks:
            if track.added_by_user_id not in all_added_by_user_ids:
                all_added_by_user_ids.append(track.added_by_user_id)

        user_id_to_user_name = SpotifyApiClient.__get_user_name_by_user_id_mapping(access_token, all_added_by_user_ids)

        for track in tracks:
            track.added_by = user_id_to_user_name[track.added_by_user_id]

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_user_name_by_user_id_mapping(access_token, all_added_by_user_ids):
        user_name_by_user_id_mapping = {}

        print(f"{LOG_PREFIX}.__get_user_name_by_user_id_mapping => "
              f"# all_added_by_user_ids: {len(all_added_by_user_ids)}")

        for user_id in all_added_by_user_ids:
            user_name = SpotifyApiClient.__get_user_name_for_user_id(access_token, user_id)
            user_name_by_user_id_mapping[user_id] = user_name

        return user_name_by_user_id_mapping

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_user_name_for_user_id(access_token, user_id):
        url = f"https://api.spotify.com/v1/users/{user_id}"
        user_data = SpotifyApiUtils.send_get_request(url, access_token)
        user_name = user_data["display_name"]

        return user_name

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __update_genres_of_tracks(tracks, access_token):
        all_artist_ids = []

        for track in tracks:
            for artist_id in track.artist_ids:
                if artist_id not in all_artist_ids:
                    all_artist_ids.append(artist_id)

        genres_by_artist_id_mapping = SpotifyApiClient.__get_genres_by_artist_id_mapping(all_artist_ids, access_token)

        for track in tracks:
            genres = SpotifyApiClient.__get_genres_of_artists(track.artist_ids, genres_by_artist_id_mapping)
            track.update_genres_and_super_genres(genres)

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_genres_by_artist_id_mapping(artist_ids, access_token):
        artist_id_to_genres = {}

        max_ids_per_request = 50
        artist_id_chunks = SpotifyApiUtils.split_list_into_chunks(artist_ids, max_ids_per_request)

        print(f"{LOG_PREFIX}.__get_genres_by_artist_id_mapping => "
              f"# artist_ids: {len(artist_ids)}, # artist_id_chunks: {len(artist_id_chunks)}")

        for curr_artist_ids in artist_id_chunks:
            curr_artist_id_to_genres = SpotifyApiClient.__get_genres_by_artist_id_mapping_for_one_request(
                curr_artist_ids, access_token)
            artist_id_to_genres.update(curr_artist_id_to_genres)

        return artist_id_to_genres

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_genres_by_artist_id_mapping_for_one_request(artist_ids, access_token):
        genres_by_artist_id_mapping = {}

        url = "https://api.spotify.com/v1/artists"
        response_data = SpotifyApiUtils.send_get_request_with_ids(url, access_token, artist_ids)
        artists = response_data["artists"]

        for artist in artists:
            artist_id = artist["id"]
            genres_by_artist_id_mapping[artist_id] = artist["genres"]

        return genres_by_artist_id_mapping

    @staticmethod
    def __get_genres_of_artists(artist_ids, genres_by_artist_id_mapping):
        genres = []

        for artist_id in artist_ids:
            genres_of_artist = genres_by_artist_id_mapping[artist_id]
            for genre in genres_of_artist:
                if genre not in genres:
                    genres.append(genre)

        return genres

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __update_audio_features_of_tracks(tracks, access_token):
        audio_features_by_track_index = SpotifyApiClient.__get_audio_features_of_tracks(tracks, access_token)

        assert len(audio_features_by_track_index) == len(tracks)

        for i in range(0, len(tracks)):
            audio_features = audio_features_by_track_index[i]
            tracks[i].update_attributes_by_audio_features(audio_features)

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_audio_features_of_tracks(tracks, access_token):
        audio_features_by_track_index = []

        track_ids = []
        for track in tracks:
            track_ids.append(track.id)

        max_ids_per_request = 100
        track_id_chunks = SpotifyApiUtils.split_list_into_chunks(track_ids, max_ids_per_request)

        len(f"{LOG_PREFIX}.__get_audio_features_of_tracks => "
            f"# tracks: {len(tracks)}, # track_id_chunks: {len(track_id_chunks)}")

        for track_ids_of_chunk in track_id_chunks:
            audio_features = SpotifyApiClient.__get_audio_features_for_one_request(
                access_token, track_ids_of_chunk)
            audio_features_by_track_index.extend(audio_features)

        return audio_features_by_track_index

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __get_audio_features_for_one_request(access_token, track_ids_of_chunk):
        url = "https://api.spotify.com/v1/audio-features"
        response_data = SpotifyApiUtils.send_get_request_with_ids(url, access_token, track_ids_of_chunk)
        audio_features = response_data["audio_features"]

        return audio_features

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __create_empty_playlist(playlist_name, user_id, access_token):
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        data = {
            "name": playlist_name,
            "public": True
        }

        response_data = SpotifyApiUtils.send_post_request(url, access_token, data)
        playlist_id = response_data["id"]

        return playlist_id

    @staticmethod
    @Utils.measure_execution_time(LOG_PREFIX)
    def __add_tracks_to_playlist(playlist_id, track_ids, access_token):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        max_ids_per_request = 100
        track_id_chunks = SpotifyApiUtils.split_list_into_chunks(track_ids, max_ids_per_request)

        len(f"{LOG_PREFIX}.__add_tracks_to_playlist => "
            f"# track_ids: {len(track_ids)}, # track_id_chunks: {len(track_id_chunks)}")

        for track_id_chunk in track_id_chunks:
            track_uris = [f"spotify:track:{track_id}" for track_id in track_id_chunk]
            data = {"uris": track_uris}
            SpotifyApiUtils.send_post_request(url, access_token, data)
