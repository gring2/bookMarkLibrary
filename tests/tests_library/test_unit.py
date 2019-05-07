from time import sleep

from bookMarkLibrary.database import db
from models import User
from library.models import Category, BookMark
from tests.base import BaseTestCase
from handlers.category_handler import fetch_sub_category
from handlers.image_handler import OgImageHandler, FaviconHandler
from unittest import mock


class CategoryHandlerTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User(id=0, email='test@test.com')

    def test_fetch_sub_category_do_not_make_root(self):
        data = fetch_sub_category(self.user)
        self.assertIsNotNone(data)
        root = Category.query.count()
        self.assertEqual(1, root)
        movie_category = Category(name="Movie", parent_id=data.id, user_id=self.user.id)
        db.session.add(movie_category)
        db.session.commit()

        fetch_sub_category(self.user, movie_category.id)
        two = Category.query.count()
        self.assertEqual(2, two)

    def test_fetch_category_with_sub_list(self):
        data = fetch_sub_category(self.user)
        self.assertIsNotNone(data)

        # add sub objects
        # Category
        # root: {name:root, id:1, sub: [root1, root2], parent_id: 0}
        # Category: {name: Movie, id: 2, sub: [4, 5 ], parent_id: 1} , SnapShot: {'id': 3, 'url': 'http://test.com', 'img': 'test.com.png', parent_id: 1}
        #   |
        # Category: {name: Hero, id: 4, sub: [0111, 0112, 0113], parent_id: 2},  Category: {name: Documentary, id: 5 , parent_id: 2}
        #   |
        # SnapShot{'url':http://ironman1.com', img: 'ironman1.png', id: 6, parent_id: 4}
        # SnapShot{'url':http://ironman1.com', img: 'ironman1.png', id: 7, , parent_id: 4}
        # SnapShot{'url':http://ironman1.com', img: 'ironman1.png', id: 8, parent_id: 4}

        movie_category = Category(name="Movie", parent_id=data.id, user_id=self.user.id)
        db.session.add(movie_category)
        db.session.commit()
        sleep(1)
        first_snapshot = BookMark(url='http://test.com', img='test.com.png', parent_id=data.id)

        hero_movie_category = Category(name="Hero", parent_id=movie_category.id, user_id=self.user.id)
        documentary_movie_category = Category(name="Documentary", parent_id=movie_category.id, user_id=self.user.id)
        db.session.add_all(
            [
                first_snapshot,
                hero_movie_category,
                documentary_movie_category,
            ]
        )

        db.session.commit()
        hero_movie_category = Category.query.filter_by(name="Hero", user_id=self.user.id).first()
        ironman_1 = BookMark(url='http://ironman1.com', img='ironman1.com.png', parent_id=hero_movie_category.id)
        ironman_2 = BookMark(url='http://ironman2.com', img='ironman2.com.png', parent_id=hero_movie_category.id)
        ironman_3 = BookMark(url='http://ironman3.com', img='ironman3.com.png', parent_id=hero_movie_category.id)

        db.session.add_all(
            [
                ironman_1,
                ironman_2,
                ironman_3
            ]
        )

        db.session.commit()
        root_with_sub_list = fetch_sub_category(self.user)
        self.assertEqual(2, len(root_with_sub_list.sub))
        self.assertTrue(type(root_with_sub_list.sub[0]) == Category)
        self.assertEqual('Movie', root_with_sub_list.sub[0].name)
        self.assertTrue(type(root_with_sub_list.sub[1]) == BookMark)
        self.assertTrue(hasattr(root_with_sub_list.sub[1], 'url'))
        self.assertEqual('http://test.com', root_with_sub_list.sub[1].url)

        movie_category_sub_list = fetch_sub_category(self.user, movie_category.id)
        self.assertEqual(2, len(movie_category_sub_list.sub))

        hero_category_with_snapshots_only = fetch_sub_category(self.user, hero_movie_category.id)
        self.assertEqual(3, len(hero_category_with_snapshots_only.sub))
        self.assertTrue(type(hero_category_with_snapshots_only.sub[0]) == BookMark)
        self.assertEqual('http://ironman1.com', hero_category_with_snapshots_only.sub[0].url)

        self.assertTrue(type(hero_category_with_snapshots_only.sub[1]) == BookMark)
        self.assertEqual('http://ironman2.com', hero_category_with_snapshots_only.sub[1].url)

        self.assertTrue(type(hero_category_with_snapshots_only.sub[2]) == BookMark)
        self.assertEqual('http://ironman3.com', hero_category_with_snapshots_only.sub[2].url)

    def tearDown(self):
        super().tearDown()


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
        bookmark.save()

        self.assertEqual('Google', bookmark.name)

    def test_blank_page_thumbnail(self):
        bookmark = BookMark()
        bookmark.url = 'https://google.com'
        bookmark.parent_id=1
        bookmark.save()
        bookmark.img = None
        db.session.add(bookmark)
        db.session.commit()

        self.assertEqual('/static/img/blank.png', bookmark.thumbnail)