from bs4 import BeautifulSoup, element
import requests
import traceback
import logging


def meta_node_ha_attri(node, attr):
    return node is not None and node.has_attr(attr)


def get_image_meta(response, target_info, attr_name):
    try:

        soup = BeautifulSoup(response.text, 'html.parser')
        node = soup.find(**target_info)

        if meta_node_ha_attri(node, attr_name) and len(node[attr_name]) > 1:
            return node

        return None

    except requests.exceptions.ConnectionError:
        logging.error(traceback.extract_stack())
        return None


class OgImageHandler():
    def __init__(self, response: requests.Response):
        self._response = response
        self._node = None
        self._content_attr_name = 'content'
        self._target_info = {
            'name': 'meta', 'attrs': {'property': 'og:image'}
        }

    def has_og_image_meta(self):
        node = get_image_meta(self._response, self._target_info, self._content_attr_name)
        if node:
            self._node = node

        return self._node is not None

    def get_url(self):
        return self._node['content']


class FaviconHandler():
    def __init__(self, response: requests.Response):
        self._response = response
        self._node = None

    def has_favicon_image_link_tag(self)->bool:
        link_tag_info = {
            'name': 'link',
            'attrs': {'rel': 'icon'}
        }
        node = get_image_meta(self._response, link_tag_info, 'href')
        if node:
            self._node = node

        return self._node is not None

    def has_image_meta_tag(self)->bool:
        link_tag_info = {
            'name': 'meta',
            'attrs': {'itemprop': 'image'}
        }
        node = get_image_meta(self._response, link_tag_info, 'content')
        if node:
            self._node = node

        return self._node is not None

    def get_url(self)->str:

        return self._favicon['content']