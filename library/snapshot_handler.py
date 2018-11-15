from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import os
from flask import current_app as app


class SnapShotHandler():
    def __init__(self) -> None:
        super().__init__()
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1800, 1200)
        self.dir = app.config['STORAGE_PATH']

        if os.path.exists(self.dir) is not True:
            os.makedirs(self.dir)

    def make_snapshot(self, url):
        try:
            if not ('http://' in url or 'https://' in url):
                url = 'http://' + url
            self.driver.get(url)
            file_name = re.sub("https?://[www]?", '', url) + '.png'
            self.driver.save_screenshot(self.dir + '/' + file_name)

        except Exception:
            return False
        return file_name
