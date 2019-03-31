from bs4 import BeautifulSoup
import requests
import traceback

class OgImageHandler():

    def __init__(self, url:str):
        self._url = url
        self._og = None

    def has_og_image_meta(self):
        try:
            response = requests.get(self._url)
            if response.status_code > 300:
                return False

            soup = BeautifulSoup(response.text, 'html.parser')
            og = soup.find('meta', {'property': 'og:image'})

            if og is None or og['content'] is None or len(og['content']) < 1:
                return False

            self._og = og

            return True
        except requests.exceptions.ConnectionError:
            print(traceback.extract_stack())
            return False

    def get_og_url(self):
        return self._og['content']