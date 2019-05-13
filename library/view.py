
from flask_security import current_user, login_required
from . import bp
from flask import (render_template, request, g, redirect, url_for)
from library.models import BookMark, Tag
from library import contract
from bookMarkLibrary.exceptions import InvalidURLException


@login_required
@bp.route('/add', methods=['POST'])
def add_ele():
    bookmark = BookMark(url=BookMark.remove_last_slash_from_url(request.form['url']))
    tags = [Tag.find_or_make(tag) for tag in request.form.getlist('tags[]')]
    try:
        bookmark.makeup()
        contract.register_bookmark_and_tag(current_user, bookmark, *tags)
    except InvalidURLException:
        pass

    return redirect(url_for('library.urls'))


@bp.route('/urls')
@login_required
def urls():
    bookMarks = current_user.bookmarks
    # flattern need
    tags = []
    for bookmark in bookMarks:
        tags.extend(bookmark.tags)

    return render_template('library/urls.html', bookmarks=bookMarks, tags=tags)


@bp.route('/thumbnail', methods=['POST'])
@login_required
def change_thumbnail():
    file = request.files['thumbnail']
    id = request.form['id']

    bookmark = BookMark.query.get(id)

    bookmark.change_thumbnail(file)

    return redirect(url_for('library.urls'))
