from handlers.og_image_handler import OgImageHandler
from handlers.screenshot_handler import ScreenShotHandler


def create_thumbnail(url:str, id:str)->str or None:
    url = get_http_format_url(url)
    og_handler = OgImageHandler(url)

    if og_handler.has_og_image_meta():
        file_name = og_handler.get_og_url()

    else:
        screenshot_handler = ScreenShotHandler()
        file_name = screenshot_handler.make_screenshot(url, id)

    return file_name


def get_http_format_url(url: str)->str:
    """
    :param url: url format(http or https may be included or not ) string
    :return: full formatted url(http[s]://[www]uri) string
    """
    if not ('http://' in url or 'https://' in url):
        url = 'http://' + url
    return url
