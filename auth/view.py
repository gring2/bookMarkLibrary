from bookMarkLibrary import user_datastore, db, User
from . import bp
from flask import (current_app as app, render_template, abort, request, redirect, url_for)
from flask_security import login_user

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_datastore.create_user(email=request.form['email'], password=request.form['password'])
        db.session.commit()
        return redirect('/')

@bp.route('login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = User(**request.form)
        login_user(user)
        return redirect('/')