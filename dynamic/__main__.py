import argparse
import os
import time

from . import crawler_util
from . import config
from . import dynamic_util
from . import storage_util


parser = argparse.ArgumentParser()
parser.add_argument("--force", help="Whether to force update picture urls.")
args = parser.parse_args()


def build_picture_urls(mid, cookie):

    # TODO: we can load the already crawled picture urls here.
    picture_urls = {}

    dynamic_api_url = dynamic_util.build_dynamic_api_url(mid)
    while dynamic_api_url != "":
        api_resp = crawler_util.fetch_dynamic_api(dynamic_api_url, cookie)
        time.sleep(3)

        current_picture_urls = dynamic_util.extract_picture_urls(api_resp)
        # TODO: we can check whether current picture urls are already crawled,
        # and break the loop early.
        picture_urls.update(current_picture_urls)

        dynamic_api_url = dynamic_util.build_next_dynamic_api_url(mid, api_resp)

    return picture_urls


def download_picture(url, pub_ts, index):
    filepath = storage_util.build_picture_filepath(url, pub_ts, index)
    if os.path.exists(filepath):
        print(f"skipped: {url} {filepath}")
        return

    picture_content = crawler_util.fetch_picture(url)
    time.sleep(1)

    storage_util.dump_picture(picture_content, filepath)


def download_pictures(picture_urls):
    for pub_ts, urls in picture_urls.items():
        for index, url in enumerate(urls):
            download_picture(url, pub_ts, index)


if __name__ == "__main__":
    picture_urls = storage_util.load_metadata()
    if not len(picture_urls) or args.force:
        picture_urls = build_picture_urls(config.MID, config.COOKIE)
    storage_util.dump_metadata(picture_urls)

    download_pictures(picture_urls)
