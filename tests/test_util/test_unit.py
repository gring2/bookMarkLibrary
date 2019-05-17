from unittest import TestCase
from utils import url_utils


class UrlUtilTest(TestCase):
    def test_get_http_format_url(self):
        expect = 'http://www.python.org'

        only_host = 'python.org'
        only_host_result = url_utils.get_http_format_url(only_host)
        self.assertEquals(expect, only_host_result)

        host_with_www = 'www.python.org'
        host_with_www_result = url_utils.get_http_format_url(host_with_www)
        self.assertEquals(expect, host_with_www_result)

        host_with_http = 'http://python.org'
        host_with_http_result = url_utils.get_http_format_url(host_with_http)
        self.assertEquals(expect, host_with_http_result)

        expect_result = url_utils.get_http_format_url(expect)
        self.assertEquals(expect, expect_result)
