from unittest.mock import patch

from handlers.thumbnail_handler import ThumbnailHandler
from tests.base import BaseTestCase
from handlers.image_handler import OgImageHandler, FaviconHandler
from unittest import mock
from library.models import BookMark
from models import User
from bookMarkLibrary.database import db


class OGHandlerTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.mock_res = mock.patch('requests.Response')

    def test_has_og_image_meta(self):
        self.mock_res.text = """
            <html>
                <head>
                    <meta property="og:image" content="testmeta"/>
                </head>
                <body>
                </body>
            </html>
        """

        handler = OgImageHandler(self.mock_res)

        result = handler.has_og_image_meta()
        self.assertTrue(result)

    def test_has_no_og_image_meta(self):
        # meta tag does not exist
        self.mock_res.text = """
            <html>
                <head>

                </head>
                <body>
                </body>
            </html>
        """
        handler = OgImageHandler(self.mock_res)
        result = handler.has_og_image_meta()
        self.assertFalse(result)

        # meta:porperty does not exist
        self.mock_res.text = """
            <html>
                <head>
                    <meta charset="utf8" content="testmeta"/>

                </head>
                <body>
                </body>
            </html>
        """
        handler = OgImageHandler(self.mock_res)
        result = handler.has_og_image_meta()
        self.assertFalse(result)

        # meta:porperty's value is not og:image
        self.mock_res.text = """
            <html>
                <head>
                    <meta property="utf8" content="testmeta"/>

                </head>
                <body>
                </body>
            </html>
        """
        handler = OgImageHandler(self.mock_res)
        result = handler.has_og_image_meta()
        self.assertFalse(result)

        # meta has property attribute but does not have content attribute
        self.mock_res.text = """
            <html>
                <head>
                    <meta property="og:image" />
                </head>
                <body>
                </body>
            </html>
        """
        handler = OgImageHandler(self.mock_res)
        result = handler.has_og_image_meta()
        self.assertFalse(result)

        # meta content attribute has not value
        self.mock_res.text = """
            <html>
                <head>
                    <meta property="og:image" content=""/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = OgImageHandler(self.mock_res)
        result = handler.has_og_image_meta()
        self.assertFalse(result)


class FaviconHandlerTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.mock_res = mock.patch('requests.Response')

    def test_has_favicon_image_link_tag(self):
        self.mock_res.text = """
            <html>
                <head>
                    <link rel="icon" href="test.com"/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)

        result = handler.set_favicon_image_link_tag()
        self.assertTrue(result)

    def test_has_no_favicon_link_tag(self):
        # link tag does not exist
        self.mock_res.text = """
            <html>
                <head>

                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_favicon_image_link_tag()
        self.assertFalse(result)

        # link:rel does not exist
        self.mock_res.text = """
            <html>
                <head>
                    <link test="test"/>

                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_favicon_image_link_tag()
        self.assertFalse(result)

        # link:ref's value is not icon
        self.mock_res.text = """
            <html>
                <head>
                    <link rel="stylesheet" href="test.icon"/>

                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_favicon_image_link_tag()
        self.assertFalse(result)

        # link has rel attribute but does not have href attribute
        self.mock_res.text = """
            <html>
                <head>
                    <link rel="icon" />
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_favicon_image_link_tag()
        self.assertFalse(result)

        # link href attribute has not value
        self.mock_res.text = """
            <html>
                <head>
                    <link rel="icon" href=""/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_favicon_image_link_tag()
        self.assertFalse(result)

    def test_has_itemprop_meta_tag(self):
        self.mock_res.text = """
            <html>
                <head>
                    <meta itemprop="image" content="testmeta"/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertTrue(result)

    def test_has_no_itemprop_meta_tag(self):
        # meta tag does not exist
        self.mock_res.text = """
            <html>
                <head>

                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertFalse(result)

        # meta:itemprop does not exist
        self.mock_res.text = """
            <html>
                <head>
                    <meta charset="utf8" content="testmeta"/>

                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertFalse(result)

        # meta:itemprop's value is not image
        self.mock_res.text = """
            <html>
                <head>
                    <meta itemprop="test" content="testmeta.icon"/>

                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertFalse(result)

        # meta has itemprop attribute but does not have content attribute
        self.mock_res.text = """
            <html>
                <head>
                    <meta itemprop="image"/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertFalse(result)

        # meta content attribute has not value
        self.mock_res.text = """
            <html>
                <head>
                    <meta itemprop="image" content=""/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertFalse(result)

    def test_get_url_return_link_ref_attrs(self):
        self.mock_res.text = """
            <html>
                <head>
                    <link rel="icon" href="test_favicon"/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_favicon_image_link_tag()
        self.assertTrue(result)
        url = handler.get_url()
        self.assertIsNotNone(url)
        self.assertEqual('test_favicon', url)

    def test_get_url_return_meta_content(self):
        self.mock_res.text = """
            <html>
                <head>
                    <meta itemprop="image" content="testmeta"/>
                </head>
                <body>
                </body>
            </html>
        """
        handler = FaviconHandler(self.mock_res)
        result = handler.set_image_meta_tag()
        self.assertTrue(result)

        url = handler.get_url()

        self.assertIsNotNone(url)
        self.assertEqual('testmeta', url)


class ThumbnailHandlerTest(BaseTestCase):

    def test_return_title_thumbnail_path(self):
        t = ThumbnailHandler('https://google.com')
        result = t.create_thumbnail()

        self.assertIsNotNone(result[1])
        self.assertIsNotNone(result[0])

    def test_sub_domain_return_title_and_thumbnail(self):
        url = 'https://www.google.com/search?' + \
                       'source=hp&ei=RT3VXIXyJfSMr7wPjI6M6Ac&q=' + \
                       'urlparse&oq=urlp&gs_l=psy-ab.1.1.0l5j0i10j0l4.2477.3781..5473...2.0..0.87.451.6......0....1..gws-wiz.....0.FWwWVpuif-g'
        t = ThumbnailHandler(url)
        result = t.create_thumbnail()

        self.assertIsNotNone(result[1])
        self.assertIsNotNone(result[0])

    @patch('handlers.thumbnail_handler.requests')
    def test_reuturn_none_thumbnail_name(self, mock_requests):
        mock_res = mock.patch('requests.Response')
        mock_res.status_code = 200
        mock_res.text = """
            <html>
                <head>
                    <meta charset="utf8" content="testmeta"/>
                    <title>
                        testTItle
                    </title>

                </head>
                <body>
                </body>
            </html>
        """
        mock_requests.get.return_value = mock_res

        t = ThumbnailHandler('test.test')
        result = t.create_thumbnail()

        self.assertEqual('testTItle', result[1].strip())
        self.assertIsNone(result[0])

    @patch('handlers.thumbnail_handler.requests')
    def test_return_og_image_first(self, mock_requests):
        mock_res = mock.patch('requests.Response')
        mock_res.status_code = 200
        mock_res.text = """
            <html>
                <head>
                    <meta property="og:image" content="testmeta"/>
                    <link rel="icon" href="test.com"/>
                    <title>
                        testTItle
                    </title>

                </head>
                <body>
                </body>
            </html>
        """
        mock_requests.get.return_value = mock_res

        t = ThumbnailHandler('test.test')
        result = t.create_thumbnail()

        self.assertEqual('testTItle', result[1].strip())
        self.assertEqual('https://testmeta', result[0].strip())

    @patch('handlers.thumbnail_handler.requests')
    def test_return_og_image(self, mock_requests):
        mock_res = mock.patch('requests.Response')
        mock_res.status_code = 200
        mock_res.text = """
            <html>
                <head>
                    <meta property="og:image" content="testmeta"/>
                    <title>
                        testTItle
                    </title>

                </head>
                <body>
                </body>
            </html>
        """
        mock_requests.get.return_value = mock_res

        t = ThumbnailHandler('http://test.test')
        result = t.create_thumbnail()

        self.assertEqual('testTItle', result[1].strip())
        self.assertEqual('https://testmeta', result[0].strip())

    @patch('handlers.thumbnail_handler.requests')
    def test_return_favicon_image(self, mock_requests):
        mock_res = mock.patch('requests.Response')
        mock_res.status_code = 200
        mock_res.text = """
            <html>
                <head>
                    <link rel="icon" href="/test.com"/>
                    <title>
                        testTItle
                    </title>

                </head>
                <body>
                </body>
            </html>
        """
        mock_requests.get.return_value = mock_res

        t = ThumbnailHandler('http://test.test')
        result = t.create_thumbnail()

        self.assertEqual('testTItle', result[1].strip())
        self.assertEqual('http://test.test/test.com', result[0].strip())
