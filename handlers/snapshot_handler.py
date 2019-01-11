from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import os
from flask import current_app as app
from PIL import Image

class SnapShotHandler():
    """ class handling snapshot make snapshot logic
    Attributes:
        __driver (str): chrome webdriver dependency
        __dir (int): path which is used to store snapshot

    """
    def __init__(self) -> None:
        super().__init__()
        options = Options()
        options.add_argument('--headless')
        self.__driver = webdriver.Chrome(options=options)
        self.__driver.set_window_size(1800, 1200)
        self.__dir = app.config['STORAGE_PATH']

        if os.path.exists(self.__dir) is not True:
            os.makedirs(self.__dir)

    def make_snapshot(self, url: str)->str or False:
        """

        :param url:
        :return file_name: name of stored snapshot png file
        """
        try:
            url = self.__get_http_format_url(url)
            self.__driver.get(url)
            file_name = self.__remove_http_protocol_string(url) + '.png'
            path = self.__dir + '/' + file_name
            self.__driver.save_screenshot(path)
            resize_img(path)

        except Exception:
            return False
        return file_name

    def __get_http_format_url(self, url: str)->str:
        """
        :param url: url format(http or https may be included or not ) string
        :return: full formatted url(http[s]://[www]uri) string
        """
        if not ('http://' in url or 'https://' in url):
            url = 'http://' + url
        return url

    def __remove_http_protocol_string(self, url: str)->str:
        """
        :param url: url format(http or https may be included or not ) string
        :return: uri (http[s]:// and www must not included )
        """
        return re.sub("https?://[www]?", '', url)


def resize_img(path)->bool:
    try:
        img = Image.open(path)
        img.resize((150, 150)).save()
        return True
    except Exception:
        return False
