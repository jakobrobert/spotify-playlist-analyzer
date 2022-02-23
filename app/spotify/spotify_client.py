import requests


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    def get_songs_of_playlist(self, playlist_id):
        access_token = self.__get_access_token()
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response_data = response.json()

        tracks = response_data["tracks"]["items"]

        songs = []

        for track in tracks:
            track_item = track["track"]

            title = track_item["name"]
            artists = SpotifyClient.__get_artists_of_track(track_item)
            duration = SpotifyClient.__get_duration_of_track(track_item)
            release_date = SpotifyClient.__get_release_date_of_track(track_item)

            song = {"artists": artists, "title": title, "duration": duration, "release_date": release_date}
            songs.append(song)

        return songs

    def __get_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        grant_type = "client_credentials"   # TODO inline var
        data = {"grant_type": grant_type}
        auth = (self.CLIENT_ID, self.CLIENT_SECRET)

        response = requests.post(url, data=data, auth=auth)
        response_data = response.json()

        return response_data["access_token"]

    @staticmethod
    def __get_artists_of_track(track):
        artists_string = ""
        artists = track["artists"]

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
