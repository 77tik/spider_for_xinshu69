# app/__init__.py

from flask import Flask, redirect, url_for
from flask_apscheduler import APScheduler
from .models import User
from .views import auth_bp,bookmarks_bp,history_bp,main_bp
#import sentry_sdk
import secrets


def create_app():
    # 连接到sentry 进行错误跟踪
    """sentry_sdk.init(
        dsn="https://083b7490226972ac677a218fbe663540@o4506851868344320.ingest.sentry.io/4506851872342017",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )"""

    app = Flask(__name__)

    scheduler = APScheduler()
    scheduler.init_app(app)

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

    @scheduler.task('cron', id='crawl_job', minute='*/30')
    def crawl_job():
        from spider_for_xinshu69.Spider.spider_article import Spider
        from spider_for_xinshu69.Spider.headers import Headers
        url = "https://www.69xinshu.com/novels/hot"
        head = Headers()
        headers = head.get_headers()
        s = Spider(headers=headers)
        s.spider(url)
    # 启动定时任务
    scheduler.start()

    return app
