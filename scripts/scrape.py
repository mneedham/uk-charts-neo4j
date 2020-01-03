from bs4 import BeautifulSoup
import glob
import json
import urllib.parse

import base64
import requests
import urllib.parse
import os
from spotify import Spotify

credentials = f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}"
spotify = Spotify(credentials)

with open("import/items.json", "w") as items_file:
    for path in glob.glob("raw/charts/*"):
        with open(path, "r") as file:
            print(path)
            soup = BeautifulSoup(file.read(), 'html.parser')
            start, end = [date.strip() for date in soup.select("p.article-date")[0].text.strip().split(" - ")]

            rows = [row for row in soup.select("table.chart-positions tr") if len(row.select("td")) == 7]

            for row in rows:
                position = row.select("span.position")[0].text
                track_link = row.select("div.track div.title a")[0]
                artist_link = row.select("div.track div.artist a")[0]
                label = row.select("div.track div.label-cat span.label")[0].text

                song = track_link.text
                artist = artist_link.text.title()
                clean_artist = " ".join([token for token in artist.replace("/", " ").split() if not token in ["Ft", "&"]])

                response = spotify.get(track_link["href"])
                items = response["tracks"]["items"]

                document = {
                    "start": start,
                    "end": end,
                    "position": int(position),
                    "track_name": track_link.text.title(),
                    "track_uri": track_link["href"],
                    "track_file_name": track_link["href"].strip("/").replace("/", "-"),
                    "artist_name": artist_link.text.title(),
                    "artist_uri": artist_link["href"],
                    "label": label.title(),
                    "duration": items[0]["duration_ms"] if len(items) > 0 else None,
                    "artists": [{"id": item["id"], "name": item["name"]} for item in items[0]["artists"]] if len(items) > 0 else []
                }
                print(document)

                items_file.write(f"{json.dumps(document)}\n")
