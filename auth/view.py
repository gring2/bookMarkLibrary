from bookMarkLibrary import user_datastore, db
from . import bp
from flask import (current_app as app, render_template, abort, request, redirect, url_for)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_datastore.create_user(email=request.form['email'], password=request.form['password'])
        db.session.commit()
        return redirect('/')