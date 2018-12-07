from library.models import Category, SnapShot


def test_library_dict_factory():
    thumbnails = Category('0', 'root', [])
    movie_category = Category('root1', 'Movie', [])
    root_snapShot = SnapShot(**{'id': 'root2', 'url': 'http://test.com', 'img': 'test.com.png'})

    hero_movie_category = Category('Movie1', 'Hero', [])
    ironman1 = SnapShot(**{'id': 'Hero1', 'url': 'http://ironman1.com', 'img': 'ironman1.com.png'})
    ironman2 = SnapShot(**{'id': 'Hero2', 'url': 'http://ironman2.com', 'img': 'ironman2.com.png'})
    ironman3 = SnapShot(**{'id': 'Hero3', 'url': 'http://ironman3.com', 'img': 'ironman3.com.png'})
    hero_movie_category.sub = [ironman1, ironman2, ironman3]
    documentary_category = Category('Movie2', 'Documentary', [])
    movie_category.sub = [hero_movie_category, documentary_category]
    thumbnails.sub = [movie_category, root_snapShot]
    test_content = {'thumbnails': thumbnails}
    return test_content
