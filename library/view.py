from . import bp
from flask import (current_app as app, render_template, abort, request, redirect, url_for)
from utils import json_handler
from utils.snapshot_handler import SnapShotHandler
from library.models import SnapShot
from library import thumbnail


@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == "GET":
        return render_template('library/add.html')

    if request.method == "POST":
        if 'url' not in request.form:
            abort(503)
        url = request.form['url']
        snapshot_handler = SnapShotHandler()
        img_name = snapshot_handler.make_snapshot(url)

        if img_name is not False:
            bookmark_obj = SnapShot(url, img_name)
            path = app.config['STORAGE_PATH'] + '/test.json'
            data = json_handler.fetch_data_obj(path)
            thumbnail.create_or_update(data['thumbnails'], bookmark_obj)
            json_handler.write_json_file(path, data)

        return redirect(url_for('library.urls'))


@bp.route('/urls')
def urls():
    path = app.config['STORAGE_PATH'] + '/test.json'
    data = json_handler.fetch_data_obj(path)
    for idx, url in enumerate(data['thumbnails']):
        pass
    return render_template('library/urls.html', urls=data)