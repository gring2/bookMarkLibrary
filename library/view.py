import os

from flask_security import current_user, login_required

from bookMarkLibrary.app import ALLOWED_EXTENSIONS
from handlers.category_handler import save_category
from . import bp
from flask import (current_app as app, render_template, request, g, redirect, url_for)
from handlers import category_handler
from library.models import BookMark, Category


@login_required
@bp.route('/add', methods=['POST'])
def add_ele():
    if request.method == "POST":
        kind = g.kind
        cat_kind = kind['category']
        book_mark_kind = kind['book_mark']
        kind_code = request.form['kind']
        if kind_code == cat_kind['code']:
            cat = save_category(current_user, parent_id=request.form['parent_id'], name=request.form['path'])
        elif kind_code == book_mark_kind['code']:
            book_mark = BookMark(parent_id=request.form['parent_id'], url=request.form['path'])
            book_mark.save()
        return redirect(url_for('library.urls'))


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
@login_required
def urls():
    category = category_handler.fetch_sub_category(current_user)

    return render_template('library/urls.html', category=category)


@bp.route('/thumbnail', methods=['POST'])
@login_required
def change_thumbnail():
    file = request.files['thumbnail']
    if file and allowed_file(file.filename):
        id = request.form['id']
        bookmark = BookMark.query.get(id)
        img_name = bookmark.img
        file.save(os.path.join(app.config['STORAGE_PATH'], img_name))
        return redirect(url_for('library.urls'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
