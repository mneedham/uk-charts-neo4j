import base64
import requests
import urllib.parse
import os
import json

class Spotify:
    def __init__(self, credentials):
        bytes = base64.b64encode(credentials.encode("utf-8"))
        encoded_credentials = str(bytes, "utf-8")

        payload = {"grant_type": "client_credentials"}
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=payload)
        self.token = response.json()["access_token"]

    def get(self, track_uri):
        track_path_name = self.track_uri_to_path(track_uri)
        if not os.path.exists(track_path_name):
            return None
        else:
            with open(track_path_name, "r") as track_file_handle:
                return json.load(track_file_handle)

    def download(self, track_uri, track, artist):
        track_path_name = self.track_uri_to_path(track_uri)
        if not os.path.exists(track_path_name):
            print(f"Downloading [{track} {artist}] from Spotify API")
            with open(track_path_name, "w") as track_file_handle:
                clean_artist = " ".join([token for token in artist.replace("/", " ").split() if not token in ["Ft", "&"]])
                query = urllib.parse.quote(f"{track} {clean_artist}")
                response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1", headers={"Authorization": f"Bearer {self.token}"})
                json.dump(response.json(), track_file_handle, indent=4)

    def track_uri_to_path(self, track_uri):
        track_file_name = track_uri.strip("/").replace("/", "-")
        return f"raw/songs/{track_file_name}"
