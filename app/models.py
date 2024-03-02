from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin


db = SQLAlchemy()


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_number'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    # 定义与 User 模型的关系
    user = db.relationship('User', backref='history')

    # 定义与 Book 模型的关系
    book = db.relationship('Books', backref='history')

    # 定义与 Chapter 模型的关系
    chapter = db.relationship('Chapters', backref='history')




class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)  # 关联的书籍 ID

    # 定义外键关系
    book = db.relationship('Books', backref='bookmarks')

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Books(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(30))
    description = db.Column(db.Text)

class Chapters(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.Integer,db.ForeignKey(Books.id),nullable = False)
    chapter_number = db.Column(db.Integer)
    title = db.Column(db.String(30))
    content = db.Column(db.Text)