from functools import wraps

from flask import session, flash, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'email' not in session:
            flash("请先登录")
            return redirect(url_for('auth.login'))
        return f(*args,**kwargs)
    return decorated_function


