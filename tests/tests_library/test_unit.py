from flask_security import login_user, url_for_security

from bookMarkLibrary.database import db
from bookMarkLibrary.models import User
from library.models import Category, SnapShot
from tests.base import BaseTestCase
from library.thumbnail import get_next_id
from handlers.category_handler import fetch_bookmark_elem


class JsonHandlerTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User(id=0,email='test@test.com', next_id=0)
        
    def test_fetch_default_category(self):
        data = fetch_bookmark_elem(self.user)
        self.assertIsNotNone(data)
        self.assertEqual(2, self.user.next_id)

    def test_fetch_category_with_sub_list(self):
        data = fetch_bookmark_elem(self.user)
        self.assertIsNotNone(data)
        self.assertEqual(2, self.user.next_id)

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

        movie_category = Category(id=get_next_id(self.user), name="Movie", parent_id=data.id, user_id=self.user.id)
        db.session.add(movie_category)
        first_snapshot = SnapShot(id=get_next_id(self.user), url='http://test.com', img='test.com.png', parent_id=data.id)
        hero_movie_category = Category(id=get_next_id(self.user), name="Hero", parent_id=movie_category.id, user_id=self.user.id)
        documentary_movie_category = Category(id=get_next_id(self.user), name="Documentary", parent_id=movie_category.id, user_id=self.user.id)
        ironman_1 = SnapShot(id=get_next_id(self.user), url='http://ironman1.com', img='ironman1.com.png', parent_id=hero_movie_category.id)
        ironman_2 = SnapShot(id=get_next_id(self.user), url='http://ironman2.com', img='ironman2.com.png', parent_id=hero_movie_category.id)
        ironman_3 = SnapShot(id=get_next_id(self.user), url='http://ironman3.com', img='ironman3.com.png', parent_id=hero_movie_category.id)

        db.session.add_all(
            [
                movie_category,
                first_snapshot,
                hero_movie_category,
                documentary_movie_category,
                ironman_1,
                ironman_2,
                ironman_3
            ]
            )
        db.session.commit()
        self.assertEqual(9, self.user.next_id)
        root_with_sub_list = fetch_bookmark_elem(self.user)
        self.assertEqual(2, len(root_with_sub_list.sub))
        self.assertTrue(type(root_with_sub_list.sub[0]) == Category)
        self.assertEqual('Movie', root_with_sub_list.sub[0].name)
        self.assertTrue(type(root_with_sub_list.sub[1]) == SnapShot)
        self.assertTrue(hasattr(root_with_sub_list.sub[1], 'url'))
        self.assertEqual('http://test.com', root_with_sub_list.sub[1].url)

        hero_category_with_snapshots_only = fetch_bookmark_elem(self.user, movie_category.id)
        self.assertEqual(3, len(hero_category_with_snapshots_only.sub))
        self.assertTrue(type(hero_category_with_snapshots_only.sub[0]) == SnapShot)
        self.assertEqual('http://ironman1.com', hero_category_with_snapshots_only.sub[0].url)

        self.assertTrue(type(hero_category_with_snapshots_only.sub[1]) == SnapShot)
        self.assertEqual('http://ironman2.com', hero_category_with_snapshots_only.sub[1].url)

        self.assertTrue(type(hero_category_with_snapshots_only.sub[2]) == SnapShot)
        self.assertEqual('http://ironman3.com', hero_category_with_snapshots_only.sub[2].url)

    def tearDown(self):
        super().tearDown()


class LibraryTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User(id=0,email='test@test.com', next_id=0)

    def test_next_id_updated(self):
        user=self.user
        login_user(user)
        self.assertEqual(0, user.next_id)
        get_next_id(self.user)
        self.assertEqual(1, user.next_id)

        # create sub-directories
        # assert they use sequential_id

        #create thumbnails 
        #assert they share sequential_id with directories above
