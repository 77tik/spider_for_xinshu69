from flask import render_template, session, redirect, url_for
from flask_jwt_extended import jwt_required

from . import history_bp
from flask_login import login_required, current_user
from ..models import History


@history_bp.route('/history')
@login_required

def history_records():
    user_email = current_user.email
    if user_email:
        contents = History.query.filter_by(user_email=user_email).order_by(History.timestamp.desc()).all()
        return render_template('history.html', contents=contents)
    else:
        return redirect(url_for('main.index'))