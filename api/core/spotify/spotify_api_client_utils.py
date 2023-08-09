import requests

from core.http_error import HttpError


class SpotifyApiClientUtils:
    @staticmethod
    def send_get_request(url, access_token, params=None):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        error = SpotifyApiClientUtils.create_http_error_from_response_data(response_data)
        if error:
            raise error

        return response_data

    @staticmethod
    def send_get_request_with_ids(url, access_token, ids):
        ids_string = ",".join(ids)
        params = {"ids": ids_string}

        return SpotifyApiClientUtils.send_get_request(url, access_token, params)

    @staticmethod
    def send_post_request(url, access_token, data):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)

        try:
            response_data = response.json()
        except Exception:
            raise HttpError(status_code=response.status_code, title="Spotify API Error", message=response.text)

        error = SpotifyApiClientUtils.create_http_error_from_response_data(response_data)
        if error:
            raise error

        return response_data

    @staticmethod
    def create_http_error_from_response_data(response_data):
        if "error" not in response_data:
            return None

        error = response_data["error"]
        status_code = error["status"]
        message = error["message"]
        title = "Spotify API Error"

        return HttpError(status_code, title, message)