from urllib.parse import urlparse


def get_http_format_url(url: str)->str:
    """
    :param url: url format(http or https may be included or not ) string
    :return: full formatted url(http[s]://[www]uri) string
    """
    if not ('http://' in url or 'https://' in url):
        url = 'http://' + url
    return url


def get_host_from_url(url: str)->str:
    parsed_url = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
