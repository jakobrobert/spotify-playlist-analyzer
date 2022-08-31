class ViewUtils:
    @staticmethod
    def get_playlist_id_from_playlist_url(playlist_url):
        start_index = playlist_url.find("playlist/") + len("playlist/")
        end_index = playlist_url.find("?")

        return playlist_url[start_index:end_index]
