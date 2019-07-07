from flask import Blueprint
bp = Blueprint('library', __name__, url_prefix='/api/library')

import library.view
