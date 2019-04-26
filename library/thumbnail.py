from library.models import BookMark, Category

"""
maybe not used any more
"""


def create_or_update(category: Category, bookmark_obj: BookMark,
                     parent_id: str):
    if type(category) is Category:
        category = __find_parent(category, parent_id)
    else:
        # init root category
        category = Category('0', 'root', [])
    category.sub.append(bookmark_obj)


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
