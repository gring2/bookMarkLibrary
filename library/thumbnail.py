from library.models import SnapShot, Category
from flask_security import current_user

def create_or_update(category: Category, bookmark_obj: SnapShot, parent_id: str):
    if type(category) is Category:
        category = __find_parent(category, parent_id)
        if category is not None:
            bookmark_obj.id = __make_next_id(category)
    else:
        # init root category
        category = Category('0', 'root', [])
        bookmark_obj.id = '01'
    category.sub.append(bookmark_obj)


def __make_next_id(category)->str:
    # return current_user.nextId++
    last_id = '0'
    if len(category.sub) > 0:
        last_id = category.sub[-1].id.replace(category.name, '')
    return category.name + str(int(last_id) + 1)


def __find_parent(category: Category, parent_id: str)->Category or None:
    if category.id == parent_id:
        return category
    elif len(category.sub) > 0:
        sub_category_list = [type(x) is Category for x in category.sub]
        for sub in sub_category_list:
            sub_parent = __find_parent(sub, parent_id)
            if sub_parent is not None:
                return sub_parent

    else:
        return None

