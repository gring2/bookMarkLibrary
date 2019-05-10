
from flask_security import current_user, login_required

from handlers.category_handler import save_category
from . import bp
from flask import (render_template, request, g, redirect, url_for)
from handlers import category_handler
from library.models import BookMark, Category
from bookMarkLibrary.exceptions import InvalidURLException


@login_required
@bp.route('/add', methods=['POST'])
def add_ele():
    if request.method == "POST":
        kind = g.kind
        cat_kind = kind['category']
        book_mark_kind = kind['book_mark']
        kind_code = request.form['kind']
        if kind_code == cat_kind['code']:
            save_category(current_user, parent_id=request.form['parent_id'], name=request.form['path'])

        elif kind_code == book_mark_kind['code']:

            book_mark = BookMark(parent_id=request.form['parent_id'], url=BookMark.remove_last_slash_from_url(request.form['path']))
            try:
                book_mark.makeup().save()
            except InvalidURLException:
                pass
                
        return redirect(url_for('library.urls', id=request.form['parent_id']))


def __get_category_list(data: Category)->list:
    current_obj = {'id': data.id, 'name': data.name}
    result = [current_obj]
    sub = []
    for item in data.sub:
        if type(item) is Category:
            sub = sub + __get_category_list(item)

    result = result + sub
    return result


@bp.route('/urls')
@bp.route('/urls/<id>')
@login_required
def urls(id=0):
    category = category_handler.fetch_sub_category(current_user, id)

    return render_template('library/urls.html', category=category)


@bp.route('/thumbnail', methods=['POST'])
@login_required
def change_thumbnail():
    file = request.files['thumbnail']
    id = request.form['id']

    bookmark = BookMark.query.get(id)

    bookmark.change_thumbnail(file)

    return redirect(url_for('library.urls'))
