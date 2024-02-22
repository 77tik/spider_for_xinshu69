from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
bookmarks_bp = Blueprint('bookmarks', __name__)
history_bp = Blueprint('history', __name__)
main_bp = Blueprint('main', __name__)

from . import auth, bookmarks, history, main
