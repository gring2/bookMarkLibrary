from time import sleep

from bookMarkLibrary.database import db
from models import User
from library.models import Category, BookMark
from tests.base import BaseTestCase
from handlers.category_handler import fetch_sub_category


class HandlerTest(BaseTestCase):
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
        first_snapshot = BookMark( url='http://test.com', img='test.com.png', parent_id=data.id)

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
