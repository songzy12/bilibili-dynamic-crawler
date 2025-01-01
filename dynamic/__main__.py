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


def build_all_metadata(mid, cookie):

    # TODO: we can load the already crawled picture urls here.
    metadata_dict = {}

    dynamic_api_url = dynamic_util.build_dynamic_api_url(mid)
    while dynamic_api_url != "":
        api_resp = crawler_util.fetch_dynamic_api(dynamic_api_url, cookie)
        time.sleep(3)

        cur_metadata = dynamic_util.parse_metadata(api_resp)
        # TODO: we can check whether current picture urls are already crawled,
        # and break the loop early.
        metadata_dict.update(cur_metadata)

        dynamic_api_url = dynamic_util.build_next_dynamic_api_url(mid, api_resp)

    return metadata_dict


def download_picture(picture_url, pub_ts, index):
    filepath = storage_util.build_picture_filepath(picture_url, pub_ts, index)
    if os.path.exists(filepath):
        print(f"skipped: {picture_url} {filepath}")
        return

    picture_content = crawler_util.fetch_picture(picture_url)
    time.sleep(1)

    storage_util.dump_picture(picture_content, filepath)


def download_pictures(metadata_dict):
    for item in metadata_dict.values():
        pub_ts = item["upload_timestamp"]
        for index, picture_url in enumerate(item["pictures"]):
            download_picture(picture_url, pub_ts, index)


if __name__ == "__main__":
    metadata_dict = storage_util.load_metadata()
    if not len(metadata_dict) or args.force:
        metadata_dict = build_all_metadata(config.MID, config.COOKIE)
    storage_util.dump_metadata(metadata_dict)

    download_pictures(metadata_dict)
