import requests
from bs4 import BeautifulSoup
import os
import datetime

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

start = datetime.date(2018,12,28)

for week in range(0,52):
    date = start + datetime.timedelta(week*7)
    print(date)
    page = f"https://www.officialcharts.com/charts/singles-chart/{date.strftime('%Y%m%d')}"
    download_file(page)
