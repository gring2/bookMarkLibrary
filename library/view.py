
from flask_security import current_user, login_required
from . import bp
from flask import (render_template, request, g, redirect, url_for)
from library.models import BookMark
from bookMarkLibrary.exceptions import InvalidURLException


@login_required
@bp.route('/add', methods=['POST'])
def add_ele():
    if request.method == "POST":
        book_mark = BookMark(parent_id=request.form['parent_id'], url=BookMark.remove_last_slash_from_url(request.form['path']))
        try:
            book_mark.makeup().save()
        except InvalidURLException:
            pass

        return redirect(url_for('library.urls', id=request.form['parent_id']))


@bp.route('/urls')
@login_required
def urls():
    bookMarks = current_user.bookmarks
    tags = set([bookMark.tags for bookMark in bookMarks])
    return render_template('library/urls.html', category=bookMarks, tags=tags)


@bp.route('/thumbnail', methods=['POST'])
@login_required
def change_thumbnail():
    file = request.files['thumbnail']
    id = request.form['id']

    bookmark = BookMark.query.get(id)

    bookmark.change_thumbnail(file)

    return redirect(url_for('library.urls'))
