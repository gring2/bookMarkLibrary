from urllib.parse import urlparse


def get_http_format_url(url: str)->str:
    """
    :param url: url format(http or https may be included or not ) string
    :return: full formatted url(http[s]://www.uri) string
    """
    https_token = 'https://'
    http_token = 'http://'
    www_token = 'www.'

    replaced_protocol = http_token

    if https_token in url:
        url = url.replace(https_token, '')
        replaced_protocol = https_token

    elif http_token in url:
        url = url.replace(http_token, '')
        replaced_protocol = http_token

    if www_token not in url:
        url = www_token + url

    url = replaced_protocol + url

    return __remove_last_slash(url)


def get_host_from_url(url: str)->str:
    parsed_url = urlparse(url)
    url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
    return __remove_last_slash(url)


def __remove_last_slash(url: str)->str:
    last_char = url[-1:]

    if last_char == '/':
        return url[:-1]
    else:
        return url
