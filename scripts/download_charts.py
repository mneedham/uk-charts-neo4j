import requests
from bs4 import BeautifulSoup
import os

def download_file(url):
    local_filename = f"raw/charts/{url.strip('/').split('/')[-1]}"
    if not os.path.exists(local_filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        # f.flush()
    return local_filename

pages = [
    "https://www.officialcharts.com/charts/singles-chart/20191122/",
    "https://www.officialcharts.com/charts/singles-chart/20191220/"
]

for page in pages:
    download_file(page)
