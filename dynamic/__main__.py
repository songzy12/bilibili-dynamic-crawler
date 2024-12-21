import argparse
import os
import requests
import time
import json

from datetime import datetime

from .config import MID, COOKIE
from .dynamic_api_util import build_dynamic_api_url, build_next_dynamic_api_url, extract_picture_urls

OUTPUT_ROOT_DIR = 'output/dynamic'
URLS_FILENAME = 'picture_urls.json'

parser = argparse.ArgumentParser()
parser.add_argument('--force', help='Whether to force update picture urls.')
args = parser.parse_args()

def extract_all_picture_urls(mid, cookie):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cookie": cookie
    }

    # TODO: we can load the already crawled picture urls here.
    picture_urls = {}

    dynamic_api_url = build_dynamic_api_url(mid)
    print(f"fetching {dynamic_api_url}")
    while dynamic_api_url != '':
        resp = requests.get(dynamic_api_url, headers=headers).json()

        current_picture_urls = extract_picture_urls(resp)
        # TODO: we can check whether current picture urls are already crawled, and break the loop early.
        picture_urls.update(current_picture_urls)

        dynamic_api_url = build_next_dynamic_api_url(mid, resp)
        print(f"fetching {dynamic_api_url}")

        time.sleep(3)

    return picture_urls


def make_parent_dirs_if_not_exist(filepath):
    parent_dir = os.path.dirname(filepath)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)


def download_picture(url, filepath):
    if os.path.exists(filepath):
        print(f"skipped: {url} {filepath}")
        return

    print(f"crawling: {url} {filepath}")

    time.sleep(1)
    response = requests.get(url)

    make_parent_dirs_if_not_exist(filepath)
    with open(filepath, "wb") as f:
        f.write(response.content)


def download_pictures(picture_urls):
    for pub_ts, urls in picture_urls.items():
        pub_dt = datetime.fromtimestamp(int(pub_ts))
        for index, url in enumerate(urls):
            picture_name = os.path.basename(url)
            download_picture(
                url,
                os.path.join(OUTPUT_ROOT_DIR, str(MID),
                             pub_dt.strftime("%Y/%m/%d_%H%M%S"),
                             f'{index}_{picture_name}'))


if __name__ == '__main__':
    picture_urls = {}

    urls_filepath = os.path.join(OUTPUT_ROOT_DIR, str(MID), URLS_FILENAME)
    if not os.path.exists(urls_filepath) or args.force:
        picture_urls = extract_all_picture_urls(MID, COOKIE)

        make_parent_dirs_if_not_exist(urls_filepath)
        with open(urls_filepath, mode='w', encoding='utf-8') as f:
            json.dump(picture_urls, f, ensure_ascii=False, indent=4)

    with open(urls_filepath) as f:
        picture_urls = json.loads(f.read())

    download_pictures(picture_urls)
