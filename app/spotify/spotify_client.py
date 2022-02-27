import requests


class SpotifyClient:
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

            title = track["name"]
            artists = SpotifyClient.__get_artists_of_track(track)
            duration = SpotifyClient.__get_duration_of_track(track)
            release_date = SpotifyClient.__get_release_date_of_track(track)

            artist_ids_of_track = SpotifyClient.__get_artist_ids_of_track(track)
            all_artist_ids.extend(artist_ids_of_track)
            # TODO optimize: only get unique artist ids, there might be multiple tracks with the same artist

            song = {"artists": artists, "title": title, "duration": duration, "release_date": release_date,
                    "artist_ids": artist_ids_of_track}
            songs.append(song)

        artist_id_to_genres = SpotifyClient.__get_artist_id_to_genres(all_artist_ids, access_token)

        # TODO clean up: extract into method?
        for song in songs:
            genres = []
            artist_ids = song["artist_ids"]

            for artist_id in artist_ids:
                genres_of_artist = artist_id_to_genres[artist_id]
                genres.extend(genres_of_artist)

            genres_string = ", ".join(genres)
            song["genres"] = genres_string

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
        artists_string = ""
        artists = track["artists"]

        # TODO clean up: use join() as for genres string
        for i in range(len(artists)):
            artist_name = artists[i]["name"]
            if i != 0:
                artists_string += ", "
            artists_string += artist_name

        return artists_string

    @staticmethod
    def __get_duration_of_track(track):
        milliseconds = track["duration_ms"]
        total_seconds = milliseconds // 1000
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        return f"{total_minutes:02d}:{remaining_seconds:02d}"

    @staticmethod
    def __get_release_date_of_track(track):
        album = track["album"]
        release_date = album["release_date"]

        return release_date

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

        # FIXME request only supports up to 50 artist ids, need to split for more
        url = "https://api.spotify.com/v1/artists"
        headers = {"Authorization": f"Bearer {access_token}"}
        """
        artist_ids_string = ",".join(artist_ids)
        params = {"ids": artist_ids_string}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if not "artists" in response_data:
            print(response_data)
            return artist_id_to_genres

        artists = response_data["artists"]
        for artist in artists:
            artist_id = artist["id"]
            artist_genres = artist["genres"]
            artist_id_to_genres[artist_id] = artist_genres
        """
        max_ids_per_request = 50
        for i in range(0, len(artist_ids), max_ids_per_request):
            end_index = min(i + max_ids_per_request, len(artist_ids))
            curr_artist_ids = artist_ids[i:end_index]
            SpotifyClient.__get_artist_id_to_genres_for_one_request(curr_artist_ids, url, headers, artist_id_to_genres)

        #SpotifyClient.__get_artist_id_to_genres_for_one_request(artist_ids, url, headers, artist_id_to_genres)

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
