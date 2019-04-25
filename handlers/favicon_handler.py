from bs4 import BeautifulSoup
import requests
import traceback


class FaviconHandler():

    def __init__(self, response:requests.Response):
        self._response = response
        self._favicon = None

    def has_favicon_image_meta(self)->bool:
        try:
            response = self._response

            soup = BeautifulSoup(response.text, 'html.parser')
            favicon = soup.find('link', {'rel': 'icon'})

            if favicon is None or favicon['href'] is None or len(favicon['href']) < 1:
                return False

            self._favicon = favicon

            return True
        except requests.exceptions.ConnectionError:
            print(traceback.extract_stack())
            return False

    def has_image_meta_tag_in_header(self)->bool:
        try:
            response = self._response

            soup = BeautifulSoup(response.text, 'html.parser')
            favicon = soup.find('meta', {'itemprop': 'image'})

            if favicon is None or favicon['content'] is None or len(favicon['content']) < 1:
                return False

            self._favicon = favicon

            return True
        except requests.exceptions.ConnectionError:
            print(traceback.extract_stack())
            return False

    def get_url(self)->str:

        return self._favicon['content']
