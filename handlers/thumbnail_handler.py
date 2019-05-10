import traceback
from bs4 import BeautifulSoup
from flask import logging
from urllib.parse import urlparse
import requests
from bookMarkLibrary.exceptions import InvalidURLException
from utils.url_utils import get_http_format_url, get_host_from_url
from handlers.image_handler import FaviconHandler, OgImageHandler


class ThumbnailHandler():
    def __init__(self, url):
        self._url = url
        # way 1 set state on bookmark has url or file
        # way 2 inject command obj      

    def create_thumbnail(self)->tuple:
        url = get_http_format_url(self._url)
        thumbnail_path = None

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise InvalidURLException('url is not valid')

        if response.status_code > 300:
            raise InvalidURLException('url is not valid')

        og_handler = OgImageHandler(response)
        favicon_handler = FaviconHandler(response)

        if og_handler.has_og_image_meta():
            thumbnail_path = og_handler.get_url()

        elif favicon_handler.has_favicon_image_link_tag() or favicon_handler.has_image_meta_tag():
            thumbnail_path = favicon_handler.get_url()

        name = self.__get_title(response)
        thumbnail_path = self.__pad_host(thumbnail_path)
        return thumbnail_path, name

    def __get_title(self, response):
        try:

            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string
        except requests.exceptions.ConnectionError:
            logging.error(traceback.extract_stack())
            return None

    def __pad_host(self, thumbnail_path):
        host = get_host_from_url(self._url)
        if host not in thumbnail_path:
            thumbnail_path = host + thumbnail_path

        return thumbnail_path
