from flask_security import current_user, login_required

from . import bp
from flask import (current_app as app, render_template, abort, request, redirect, url_for)
from handlers import category_handler
from handlers.snapshot_handler import SnapShotHandler
from library.models import SnapShot, Category
from library import thumbnail


#dummy json path
def dummy_path():
    return app.config['STORAGE_PATH'] + '/test.json'


@bp.route('/url', methods=('GET', 'POST'))
def input_url():
    if request.method == "GET":
        return render_template('library/input_url.html')

    if request.method == "POST":
        if 'url' not in request.form:
            abort(503)
        url = request.form['url']
        parent_id = request.form['parent']
        snapshot_handler = SnapShotHandler()
        img_name = snapshot_handler.make_snapshot(url)

        if img_name is not False:
            bookmark_obj = SnapShot(None, url=url, img=img_name)
            data = category_handler.fetch_bookmark_elem(current_user)
            thumbnail.create_or_update(data['thumbnails'], bookmark_obj, parent_id)

        return redirect(url_for('library.urls'))


@bp.route('/category')
def input_category():
    if request.method == 'GET':
        fetch_obj = category_handler.fetch_bookmark_elem(current_user)
        categorys = __get_category_list(fetch_obj['thumbnails'])
        return render_template('library/input_category.html', categorys=categorys)
    if request.method == "POST":
        pass


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
    fetch_obj = category_handler.fetch_bookmark_elem(current_user)
    #data = fetch_obj['thumbnails'].sub
    return render_template('library/urls.html', thumbnails={})