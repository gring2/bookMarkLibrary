from . import bp
from flask import (current_app as app, render_template, abort, request, redirect)
import json
import traceback
from library import json_handler


@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == "GET":
        return render_template('library/add.html')

    if request.method == "POST":
        if 'url' not in request.form:
            abort(503)
        url = request.form['url']

        path = app.config['STORAGE_PATH'] + '/test.json'
        data = json_handler.get_data_obj(path)

        if 'url' in data and type(data['url']) is not list:
            urls = [data['url'], url]
            data['url'] = urls
        elif 'url' not in data:
            data['url'] = [url]
        else:
            data['url'].append(url)
        json_handler.write_json_file(path, data)

        return redirect('.')