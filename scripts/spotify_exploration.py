import base64
import requests
import urllib.parse
import json
import os

credentials = f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}"
encoded_credentials = str(base64.b64encode(credentials.encode("utf-8")), "utf-8")

payload = {"grant_type": "client_credentials"}
headers = {"Authorization": f"Basic {encoded_credentials}"}

response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=payload).json()

print("Response:", response)

token = response["access_token"]

headers = {"Authorization": f"Bearer {token}"}

track_response = requests.get("https://api.spotify.com/v1/tracks/2XU0oxnq2qxCpomAAuJY8K", headers=headers).json()
print("Track Response:", json.dumps(track_response))
