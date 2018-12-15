from flask_security import current_user
from bookMarkLibrary.database import db
from bookMarkLibrary.models import User
from library.models import SnapShot, Category

from library.thumbnail import get_next_id


def fetch_bookmark_elem(user: User, parent_id=0) -> Category:
    """
        return Category obj :
            if not exists:
                return Category(name: root, id: 1, parent_id: 0, user_id: current_user.id)
            if exists:
                return with sub list
    """
    t = current_user
    category = Category.query.filter_by(parent_id=parent_id, user_id=user.id).first()
    if category is None:
        parent_id = get_next_id(user)
        category = Category(id=get_next_id(user), name='root', parent_id=parent_id, user_id=user.id)
        db.session.add(category)
        db.session.commit()
    else:
        sub_category = Category.query.filter_by(parent_id=category.id, user_id=user.id).all()
        snapshots = SnapShot.query.filter_by(parent_id=category.id).all()
        category.sub = [*sub_category, *snapshots]
    return category
