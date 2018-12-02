from library.models import SnapShot, Category


def create_or_update(category: Category, bookmark_obj: SnapShot, parent_id: str):
    if type(category) is Category:
        category = __find_parent(category, parent_id)
        bookmark_obj.id = category.id + str(len(category.sub) + 1)
    else:
        category = Category('0', 'root', [])
        bookmark_obj.id = '01'
    category.sub.append(bookmark_obj)


def __find_parent(category: Category, parent_id: str)->Category or None:
    if category.id == parent_id:
        return category
    elif len(category.sub) > 0:
        for sub_cat in category.sub:
            sub_parent = __find_parent(sub_cat, parent_id)
            if sub_parent is not None:
                return sub_parent

    else:
        return None
