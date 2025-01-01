import requests
from . import constant


def fetch_dynamic_api(api_url, cookie):
    headers = constant.HEADERS_TEMPLATE
    headers["Cookie"] = cookie

    print(f"fetching {api_url}")
    return requests.get(api_url, headers=headers).json()


def fetch_picture(picture_url):
    print(f"crawling: {picture_url}")
    return requests.get(picture_url).content
