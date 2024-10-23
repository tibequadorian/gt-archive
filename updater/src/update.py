from datetime import datetime, timedelta, timezone
import os
import re
import subprocess
import sys
import time

from bs4 import BeautifulSoup
import dateutil.parser
import feedparser
import requests


data_path = "/data"

feed_url = "https://www.goettinger-tageblatt.de/arc/outboundfeeds/rss/"
feed = feedparser.parse(feed_url)

last_timestamp_filepath = f'{data_path}/last_timestamp'
last_timestamp = None
if os.path.exists(last_timestamp_filepath):
    with open(last_timestamp_filepath, 'r') as last_timestamp_file:
        last_timestamp = int(last_timestamp_file.read().strip())
        last_timestamp = datetime.fromtimestamp(last_timestamp, timezone.utc)
else:
    last_timestamp = datetime.now(timezone.utc) - timedelta(hours=1)

for entry in feed['entries'][::-1]:
    # skip old entries
    time_published = dateutil.parser.parse(entry['published'])
    if time_published <= last_timestamp:
        continue

    # skip if exists
    url = entry['link']
    print(f"processing {url}")
    out_filename = url.split('-')[-1]
    out_filepath = f'{data_path}/archive/{out_filename}'
    if os.path.exists(out_filepath):
        print(f"  {out_filename} already exists, skipping")
        continue

    # process url
    singlefile = subprocess.run(['npx', 'single-file', '--dump-content', url], capture_output=True).stdout
    soup = BeautifulSoup(singlefile, 'html.parser')

    # detect exclusive access
    content = soup.find(id='contentMain')
    if content and re.search('Kostenfrei bis ..:.. Uhr lesen', content.text):
        print("  exclusive access detected")

    # remove cookie popup
    for target_element in soup.find_all(id=re.compile(r'^sp_message_container_\d+$')):
        target_element.decompose()
    singlefile = str(soup)

    # save to file
    with open(out_filepath, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"  saved to {out_filename}")

    # update last timestamp
    with open(last_timestamp_filepath, 'w') as last_timestamp_file:
        last_timestamp_file.write(str(int(time_published.timestamp())))
