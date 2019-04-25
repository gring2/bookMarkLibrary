from handlers.og_image_handler import OgImageHandler
from handlers.favicon_handler import FaviconHandler
from urllib.parse import urlparse
import requests


def create_thumbnail(url:str)->str or None:
    url = get_http_format_url(url)
    response = requests.get(url)
    thumbnail_path = None

    if response.status_code > 300:
        return None

    og_handler = OgImageHandler(response)
    favicon_handler = FaviconHandler(response)

    if og_handler.has_og_image_meta():
        thumbnail_path = og_handler.get_url()

    elif favicon_handler.has_favicon_image_meta() or favicon_handler.has_image_meta_tag_in_header():
        thumbnail_path = favicon_handler.get_url()

    if thumbnail_path is not None and is_subpath(thumbnail_path):
        thumbnail_path = get_host(url) + thumbnail_path

    return thumbnail_path


def get_http_format_url(url: str)->str:
    """
    :param url: url format(http or https may be included or not ) string
    :return: full formatted url(http[s]://[www]uri) string
    """
    if not ('http://' in url or 'https://' in url):
        url = 'http://' + url
    return url


def is_subpath(url: str)->bool:
    return url[0] == '/'


def get_host(url: str)->str:
    parsed_url =  urlparse(url, '/')
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
