from flask import render_template, session, redirect, url_for
from . import history_bp
from .logrequired import login_required
from ..models import History


@history_bp.route('/history')
@login_required
def history_records():
    user_email = session.get('email')
    if user_email:
        contents = History.query.filter_by(user_email=user_email).order_by(History.timestamp.desc()).all()
        return render_template('history.html', contents=contents)
    else:
        return redirect(url_for('main.index'))