from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from flask import current_app as app
from PIL import Image


class ScreenShotHandler():
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

    def make_screenshot(self, url: str, bookmark_id:str)-> str or False:
        """

        :param url:
        :return file_name: name of stored snapshot png file
        """
        try:
            self.__driver.get(url)
            file_name = str(bookmark_id) + '.png'
            path = self.__dir + '/' + file_name
            self.__driver.save_screenshot(path)

            resize_img(path)
            result = file_name
        except Exception:
            result = False
        finally:
            self.__driver.close()
            self.__driver.quit()
            self.__driver = None
            return result



def resize_img(path)->bool:
    try:
        img = Image.open(path)
        img.resize((150, 150)).save()
        return True
    except Exception:
        return False
