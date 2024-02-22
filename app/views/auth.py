from flask import render_template, request, flash, redirect, url_for, session
from . import auth_bp
from ..models import db
from ..models import User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # 检查密码是否匹配
        if password != password2:
            flash('两次密码不匹配！', 'error')
            return redirect(url_for('auth.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("该邮箱已经被注册过","error")
            return redirect(url_for('auth.register'))

        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('注册成功，请登录！', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# 登录路由
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # 查询用户是否存在
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            flash('登录成功！', 'success')
            session['email'] = user.email
            # 这里可以设置登录状态
            return redirect(url_for('main.index'))
        else:
            flash('邮箱或密码错误！', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('email',None)
    flash('已退出登录')
    return redirect(url_for('auth.login'))

