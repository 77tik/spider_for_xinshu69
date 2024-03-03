from flask import render_template, session, flash, redirect, url_for, request, jsonify


from . import bookmarks_bp
from flask_login import login_required, current_user
from ..models import db
from ..models import Bookmark, Books


@bookmarks_bp.route('/bookmarks')
@login_required

def bookmarks():
    user_email = current_user.email
    bookmarks = Bookmark.query.filter_by(user_email=user_email).all()
    return render_template('bookmarks.html', bookmarks=bookmarks)

# 删除收藏路由
@bookmarks_bp.route('/remove_bookmark/<int:bookmark_id>', methods=['POST'])
@login_required

def remove_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    db.session.delete(bookmark)
    db.session.commit()
    flash('收藏已移除！', 'success')
    return redirect(url_for('bookmarks.bookmarks'))


@bookmarks_bp.route('/toggle_bookmark/<int:article_id>', methods=['POST'])
@login_required

def toggle_bookmark(article_id):
    # 获取当前用户的邮箱，这里假设你已经实现了用户认证和登录功能
    user_email = current_user.email

    # 获取文章对象
    article = Books.query.get_or_404(article_id)

    # 检查用户是否已经收藏了该文章
    bookmark = Bookmark.query.filter_by(user_email=user_email, book_id=article_id).first()

    # 如果用户已经收藏了文章，并且当前点击的是取消收藏，则删除该收藏记录
    if bookmark and not request.json['checked']:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'success': True})

    # 如果用户没有收藏文章，并且当前点击的是收藏，则创建一条新的收藏记录
    if not bookmark and request.json['checked']:
        bookmark = Bookmark(user_email=user_email, book_id=article_id)
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({'success': True})

    # 如果以上条件都不满足，则返回操作失败
    return jsonify({'success': False})
