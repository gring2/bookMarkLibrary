from bs4 import BeautifulSoup
import requests
import traceback


class OgImageHandler():

    def __init__(self, response:requests.Response):
        self._response = response
        self._og = None

    def has_og_image_meta(self):
        try:
            response = self._response

            soup = BeautifulSoup(response.text, 'html.parser')
            og = soup.find('meta', {'property': 'og:image'})

            if og is None or og['content'] is None or len(og['content']) < 1:
                return False

            self._og = og

            return True
        except requests.exceptions.ConnectionError:
            print(traceback.extract_stack())
            return False

    def get_url(self):
        return self._og['content']
