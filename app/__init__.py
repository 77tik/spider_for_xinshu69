# app/__init__.py

from flask import Flask, redirect, url_for

from .models import User
from .views import auth_bp,bookmarks_bp,history_bp,main_bp
from flask_jwt_extended import JWTManager
import secrets


def create_app():
    app = Flask(__name__)

    secret_key = secrets.token_hex(32)
    # 加载配置信息
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xq200431@127.0.0.1:3306/novels'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    from .models import db
    db.init_app(app)
    from .user_login import login_manager
    login_manager.init_app(app)



    # 导入并注册蓝图

    app.register_blueprint(auth_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(main_bp)

    return app
