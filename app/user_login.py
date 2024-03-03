from flask import redirect, url_for
from flask_login import LoginManager, UserMixin
from .models import User


# 创建一个 Flask-Login 的 LoginManager 实例
login_manager = LoginManager()

# 初始化 login_manager，将其与 Flask 应用实例绑定
#login_manager.init_app(app)

# 定义 user_loader 函数，用于加载用户对象
@login_manager.user_loader
def load_user(user_id):
    # 根据用户 ID 加载相应的用户对象
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    # 重定向到登录页面
    return redirect(url_for('auth.login'))
