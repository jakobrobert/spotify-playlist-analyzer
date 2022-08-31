class ViewUtils:
    @staticmethod
    def get_playlist_id_from_playlist_url(playlist_url):
        start_index = playlist_url.find("playlist/") + len("playlist/")
        end_index = playlist_url.find("?")

        return playlist_url[start_index:end_index]

    @staticmethod
    def get_attribute_display_name(attribute_name, api_client):
        attributes = api_client.get_valid_attributes_for_attribute_distribution()

        for attribute in attributes:
            if attribute["name"] == attribute_name:
                return attribute["display_name"]

        raise ValueError(f"Invalid attribute: '{attribute_name}'")
