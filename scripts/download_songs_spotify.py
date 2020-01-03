from bs4 import BeautifulSoup
import glob
import json
import urllib.parse

import base64
import requests
import os

from spotify import Spotify

credentials = f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}"
spotify = Spotify(credentials)

for path in glob.glob("raw/charts/*"):
    with open(path, "r") as file:
        print(path)
        soup = BeautifulSoup(file.read(), 'html.parser')
        rows = [row for row in soup.select("table.chart-positions tr") if len(row.select("td")) == 7]
        for row in rows:
            track_link = row.select("div.track div.title a")[0]
            track = track_link.text.title()
            artist_link = row.select("div.track div.artist a")[0]
            artist = artist_link.text.title()
            print(track, artist)
            spotify.download(track_link["href"], track, artist)
