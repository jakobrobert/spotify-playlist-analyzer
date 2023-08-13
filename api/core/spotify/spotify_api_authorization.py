from urllib.parse import urlencode

import requests

from core.http_error import HttpError
from core.spotify.spotify_api_utils import SpotifyApiUtils
from core.utils import Utils

LOG_PREFIX = "SpotifyApiAuthorization."


class SpotifyApiAuthorization:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_access_token_by_client_credentials(self):
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        auth = (self.client_id, self.client_secret)
        response = requests.post(url, data=data, auth=auth)
        response_data = response.json()

        error = SpotifyApiUtils.create_http_error_from_response_data(response_data)
        if error:
            raise error

        return response_data["access_token"]

    # TODOLATER #171 Fix: Get access token by refresh token fails
    @Utils.measure_execution_time(LOG_PREFIX)
    def get_access_token_by_refresh_token(self, refresh_token):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {self.client_id}:{self.client_secret}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        if "error" in response_data:
            error_title = "Spotify API Error: Failed to get access token by refresh token"
            # This is different to other endpoints, cannot use create_http_error_from_response_data here
            error_message = response_data["error"]
            raise HttpError(response.status_code, error_title, error_message)

        return response_data["access_token"]

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_authorization_url(self):
        authorization_base_url = "https://accounts.spotify.com/authorize"
        # TODOLATER #171 can use url_for, need to set _external=True
        # First thought that cannot use url_for to get redirect uri because url_for just returned part of the url
        # Therefore hardcoded it in ini file.
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "playlist-modify-public"
        }
        params_encoded = urlencode(params)
        authorization_url = f"{authorization_base_url}?{params_encoded}"

        return authorization_url

    @Utils.measure_execution_time(LOG_PREFIX)
    def get_access_and_refresh_token(self, authorization_code):
        token_url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(token_url, data=data, headers=headers)
        response_data = response.json()

        if "error" in response_data:
            raise HttpError(
                status_code=response.status_code,
                title=response_data["error"], message=response_data["error_description"])

        return response_data
