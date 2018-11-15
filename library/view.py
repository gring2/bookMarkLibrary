from . import bp
from flask import (current_app as app, render_template, abort, request, redirect, url_for)
from library import json_handler
from library.snapshot_handler import SnapShotHandler


@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == "GET":
        return render_template('library/add.html')

    if request.method == "POST":
        if 'url' not in request.form:
            abort(503)
        url = request.form['url']
        snapshot_handler = SnapShotHandler()
        result = snapshot_handler.make_snapshot(url)
        if result is not False:
            path = app.config['STORAGE_PATH'] + '/test.json'
            data = json_handler.get_data_obj(path)
            bookmark_obj = {url: result}

            if 'url' in data and type(data['url']) is dict:
                data['url'].update(bookmark_obj)
            elif 'url' not in data:
                data['url'] = bookmark_obj
            json_handler.write_json_file(path, data)

        return redirect(url_for('library.urls'))


@bp.route('/urls')
def urls():
    path = app.config['STORAGE_PATH'] + '/test.json'
    data = json_handler.get_data_obj(path)
    for idx, url in enumerate(data['url']):
        pass
    return render_template('library/urls.html', urls=data)