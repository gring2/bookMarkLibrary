import requests
from utils.url_utils import get_http_format_url
from utils.html_utils import get_html_node


class OgImageHandler():
    def __init__(self, response: requests.Response):
        self._response = response
        self._node = None
        self._content_attr_name = 'content'
        self._target_info = {
            'name': 'meta', 'attrs': {'property': 'og:image'}
        }

    def has_og_image_meta(self):
        node = get_html_node(self._response, self._target_info, self._content_attr_name)
        if node:
            self._node = node

        return self._node is not None

    def get_url(self):
        return get_http_format_url(self._node['content'])


class FaviconHandler():
    def __init__(self, response: requests.Response):
        self._response = response
        self._node = None

    def set_favicon_image_link_tag(self)->bool:
        link_tag_info = {
            'name': 'link',
            'attrs': {'rel': 'icon'}
        }
        node = get_html_node(self._response, link_tag_info, 'href')
        if node:
            self._node = node

        return self._node is not None

    def set_image_meta_tag(self)->bool:
        link_tag_info = {
            'name': 'meta',
            'attrs': {'itemprop': 'image'}
        }
        node = get_html_node(self._response, link_tag_info, 'content')
        if node:
            self._node = node

        return self._node is not None

    def get_url(self)->str or None:

        url = None
        try:
            url = self._node['content']

        except KeyError:
            url = self._node['href']

        finally:

            return url
