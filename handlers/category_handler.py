from bookMarkLibrary.database import db
from models import User
from library.models import BookMark, Category


def fetch_sub_category(user: User, id=0) -> Category:
    """
        return Category obj :
            if not exists:
                return Category(name: root, id: 1, parent_id: 0, user_id: current_user.id)
            if exists:
                return with sub list
    """
    if id == 0 :
        category = Category.query.filter_by(parent_id=id, user_id=user.id).first()

    else:
        category = Category.query.filter_by(id=id, user_id=user.id).first()
    if category is None:
        category = save_category(user, id, 'root')
    else:
        sub_category = Category.query.filter_by(parent_id=category.id, user_id=user.id).all()
        snapshots = BookMark.query.filter_by(parent_id=category.id).all()
        category.sub = [*sub_category, *snapshots]
        category.sub.sort(key=lambda k: k.updated_at)
    return category


def save_category(user: User, parent_id: int, name: str):
    try:
        category = Category( name=name, parent_id=parent_id, user_id=user.id)
        db.session.add(category)
        db.session.commit()
        return category

    except Exception:
        db.session.rollback()
        return False
