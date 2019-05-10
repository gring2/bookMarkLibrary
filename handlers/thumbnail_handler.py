import traceback
from bs4 import BeautifulSoup
from flask import logging
from urllib.parse import urlparse
import requests
from bookMarkLibrary.exceptions import InvalidURLException

from handlers.image_handler import FaviconHandler, OgImageHandler


def create_thumbnail(url: str)->tuple or None:
    url = get_http_format_url(url)
    response = requests.get(url)
    thumbnail_path = None
    if response.status_code > 300:
        raise InvalidURLException('url is not valid')

    og_handler = OgImageHandler(response)
    favicon_handler = FaviconHandler(response)

    if og_handler.has_og_image_meta():
        thumbnail_path = og_handler.get_url()

    elif favicon_handler.has_favicon_image_link_tag() or favicon_handler.has_image_meta_tag():
        thumbnail_path = favicon_handler.get_url()

    name = __get_title(response)

    return thumbnail_path, name


def __get_title(response):
    try:

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.string
    except requests.exceptions.ConnectionError:
        logging.error(traceback.extract_stack())
        return None


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
    parsed_url = urlparse(url, '/')
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
