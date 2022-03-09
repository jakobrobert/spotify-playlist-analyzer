import requests


class SpotifyClient:
    KEY_NAMES = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]

    def __init__(self, client_id, client_secret):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    def get_songs_of_playlist(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        access_token = self.__get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response_data = response.json()

        track_item = response_data["tracks"]["items"]

        songs = []
        all_artist_ids = []

        for track_item in track_item:
            track = track_item["track"]

            track_id = track["id"]
            title = track["name"]
            artists = SpotifyClient.__get_artists_of_track(track)
            duration = SpotifyClient.__get_duration_of_track(track)
            year_of_release = SpotifyClient.__get_year_of_release_of_track(track)

            artist_ids_of_track = SpotifyClient.__get_artist_ids_of_track(track)
            all_artist_ids.extend(artist_ids_of_track)

            # TODO refactor: define song as empty {}, then define each attribute, e.g. song["title"] = ...
            song = {"track_id": track_id, "title": title, "artists": artists, "duration": duration,
                    "year_of_release": year_of_release, "artist_ids": artist_ids_of_track}
            songs.append(song)

        artist_id_to_genres = SpotifyClient.__get_artist_id_to_genres(all_artist_ids, access_token)

        for song in songs:
            song["genres"] = SpotifyClient.__get_genres_of_artists(song["artist_ids"], artist_id_to_genres)

        SpotifyClient.__set_audio_features_of_songs(songs, access_token)

        return songs

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

        return ", ".join(artist_names)

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
            artist_id = artist["id"]
            artist_genres = artist["genres"]
            artist_id_to_genres[artist_id] = artist_genres

    @staticmethod
    def __get_genres_of_artists(artist_ids, artist_id_to_genres):
        genres = []

        for artist_id in artist_ids:
            genres_of_artist = artist_id_to_genres[artist_id]
            genres.extend(genres_of_artist)

        return ", ".join(genres)

    @staticmethod
    def __set_audio_features_of_songs(songs, access_token):
        track_ids = []

        for song in songs:
            track_ids.append(song["track_id"])

        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {access_token}"}
        # TODO #5 once more than 100 songs are supported, separate into several requests as done for genres
        track_ids_string = ','.join(track_ids)
        params = {"ids": track_ids_string}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        all_audio_features = response_data["audio_features"]

        assert len(all_audio_features) == len(songs)

        for i in range(0, len(all_audio_features)):
            audio_features = all_audio_features[i]
            song = songs[i]
            song["tempo"] = SpotifyClient.__get_tempo_from_audio_features(audio_features)
            song["key"] = SpotifyClient.__get_key_from_audio_features(audio_features)
            song["mode"] = SpotifyClient.__get_mode_from_audio_features(audio_features)
            song["loudness"] = SpotifyClient.__get_loudness_from_audio_features(audio_features)

    @staticmethod
    def __get_tempo_from_audio_features(audio_features):
        tempo = audio_features["tempo"]

        return f"{tempo:.1f}"

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

    @staticmethod
    def __get_loudness_from_audio_features(audio_features):
        loudness = audio_features["loudness"]

        return f"{loudness:.1f}"
