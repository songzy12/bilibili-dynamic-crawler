DYNAMIC_API_ROOT = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space'


def build_dynamic_api_url(mid, offset=""):
    if offset:
        return f"{DYNAMIC_API_ROOT}?host_mid={mid}&offset={offset}"
    return f"{DYNAMIC_API_ROOT}?host_mid={mid}"


def has_more(resp):
    return resp['data']['has_more']


def build_next_dynamic_api_url(mid, resp):
    if not has_more(resp):
        return ''
    return build_dynamic_api_url(mid, resp['data']['offset'])


def extract_picture_urls(resp):
    picture_urls = {}

    for item in resp['data']['items']:
        if item['type'] != 'DYNAMIC_TYPE_DRAW':
            continue
        module_author = item['modules']['module_author']
        module_dynamic_items = item['modules']['module_dynamic']['major'][
            'draw']['items']
        picture_urls[module_author['pub_ts']] = [
            module_dynamic_item['src']
            for module_dynamic_item in module_dynamic_items
        ]

    return picture_urls
