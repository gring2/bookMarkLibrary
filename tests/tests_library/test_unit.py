from models import User
from tests.base import BaseTestCase
from handlers.image_handler import OgImageHandler, FaviconHandler
from unittest import mock
from library.models import BookMark, Tag
from bookMarkLibrary.database import db
from library import contract


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

        result = handler.has_favicon_image_link_tag()
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
        result = handler.has_favicon_image_link_tag()
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
        result = handler.has_favicon_image_link_tag()
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
        result = handler.has_favicon_image_link_tag()
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
        result = handler.has_favicon_image_link_tag()
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
        result = handler.has_favicon_image_link_tag()
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
        result = handler.has_image_meta_tag()
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
        result = handler.has_image_meta_tag()
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
        result = handler.has_image_meta_tag()
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
        result = handler.has_image_meta_tag()
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
        result = handler.has_image_meta_tag()
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
        result = handler.has_image_meta_tag()
        self.assertFalse(result)

    def test_set_name_with_title_tag(self):
        bookmark = BookMark()
        bookmark.url = 'https://google.com'
        bookmark.makeup()

        self.assertEqual('Google', bookmark.name)

    def test_blank_page_thumbnail(self):
        u1 = User()
        bookmark = BookMark()
        bookmark.url = 'https://google.com'
        bookmark.makeup()
        bookmark.img = None
        u1.create_bookmarks(bookmark)
        db.session.commit()
        self.assertEqual('/static/img/blank.png', bookmark.thumbnail)

    def test_google_favicon(self):
        bookmark = BookMark()
        bookmark.url = 'https://www.google.com/search?' + \
                       'source=hp&ei=RT3VXIXyJfSMr7wPjI6M6Ac&q=' + \
                       'urlparse&oq=urlp&gs_l=psy-ab.1.1.0l5j0i10j0l4.2477.3781..5473...2.0..0.87.451.6......0....1..gws-wiz.....0.FWwWVpuif-g'
        bookmark.makeup()
        self.assertIsNotNone(bookmark.img)
        self.assertTrue('google.com' in bookmark.img)


class BookmarkTagRelTest(BaseTestCase):
    def test_tag_bookmark_relation(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        b2 = BookMark(url='python.org')
        u1.create_bookmarks(b1, b2)
        t1 = Tag(tag='tag1')
        t2 = Tag(tag='tag2')
        b1.tags.extend([t1, t2])
        t2.bookmarks.extend([b1, b2])

        db.session.add_all([u1, b1, b2, t1, t2])
        db.session.commit()

        self.assertEqual(2, len(u1.bookmarks))
        self.assertEqual(u1, b1.holder)
        self.assertEqual(u1, b1.holder)
        self.assertEqual(2, len(b1.tags))
        self.assertEqual(2, len(t2.bookmarks))
        self.assertEqual(1, len(b2.tags))
        self.assertEqual(1, len(t1.bookmarks))


class LibraryContactTest(BaseTestCase):
    def test_register_bookmark_and_tag(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag(tag='tag1')
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertEqual(b1, u1.bookmarks[0])
        self.assertEqual(2, len(u1.bookmarks[0].tags))

    def test_register_bookmark_and_tag_rollback(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag()
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertIsNone(u1.bookmarks[0].id)
        self.assertEqual(0, Tag.query.count())
        self.assertEqual(0, BookMark.query.count())


