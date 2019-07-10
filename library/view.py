import json
from flask_security import current_user, login_required, auth_token_required
from . import bp
from flask import (jsonify, request, g, redirect, url_for)
from library.models import BookMark, Tag
from library import contract
from bookMarkLibrary.exceptions import InvalidURLException
from utils.url_utils import get_http_format_url


@auth_token_required
@bp.route('/add', methods=['POST'])
def add_ele():
    result = True
    code = 200
    try:
        bookmark = BookMark(url=get_http_format_url(request.json.get('url', '')))

        tag_inputs = Tag.conv_tag_str_to_list(request.json.get('tags', ''))

        tags = [Tag.find_or_make(tag) for idx, tag in enumerate(tag_inputs)]
        bookmark.makeup()
        contract.register_bookmark_and_tag(current_user, bookmark, *tags)

    except InvalidURLException:
        result = False
        code = 500
    finally:

        return json.dumps({'success': result}), code, {'ContentType': 'application/json'}


@bp.route('/urls')
@bp.route('/urls/<string:tag>')
@auth_token_required
def urls(tag=None):
    book_marks = current_user.bookmarks

    ids = [bookmark.id for bookmark in book_marks]
    tags = Tag.get_lists(ids)

    if tag is not None:
        book_marks = book_marks.join(Tag.bookmarks).filter(Tag.tag == tag)

    book_marks = book_marks.order_by(BookMark.id).all()

    tag_json = [tag.as_dict() for tag in tags]

    bookmarks_json = [bookmark.as_dict() for bookmark in book_marks]

    return jsonify({'tags': tag_json, 'bookmarks': bookmarks_json})


@bp.route('/thumbnail', methods=['POST'])
@login_required
def change_thumbnail():
    file = request.files['thumbnail']
    id = request.form['id']

    bookmark = BookMark.query.get(id)

    contract.change_thumbnail(bookmark, file)

    return redirect(url_for('library.urls'))
