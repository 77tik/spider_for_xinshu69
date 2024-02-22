from flask import render_template, request, redirect, url_for, jsonify, session
from . import main_bp
from .logrequired import login_required
from ..models import db
from ..models import Books, Chapters, History


@main_bp.route('/')
@login_required
def index():
    return render_template('thefirst.html')


@main_bp.route('/search')
@login_required
def search():
    query = request.args.get('query')
    if query:
        book_results = Books.query.filter(Books.title.like(f'%{query}%')).all()
        if book_results:
            book_id = book_results[0].id
            return redirect(url_for('main.article',id=book_id))

    else:
        return redirect(url_for('main.index'))
    return render_template('thefirst.html',not_found=True)




@main_bp.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    query = request.args.get('query')
    if query:
        # 在书籍表中搜索含有关键词的记录
        books = Books.query.filter(Books.title.like(f'%{query}%')).all()
        # 提取匹配的书籍标题
        book_titles = [book.title for book in books]
        return jsonify(book_titles)
    return jsonify([])  # 如果搜索关键词为空，返回空列表






@main_bp.route('/articles')
@login_required
def articles():
    '''db = MysqlUtil()
    sql = 'select * from books order by id DESC limit 5'
    articles = db.fetchall(sql)'''
    articles = Books.query.all()
    if articles:
        return render_template('novels.html',articles=articles)
    else:
        msg = '暂无'
        return render_template('novels.html',msg=msg)


@main_bp.route('/article/<string:id>/')
@login_required
def article(id):
    '''db = MysqlUtil()
    sql = "select chapter_number from chapters where id = '%s'" % id
    chapters = db.fetchall(sql)'''
    chapters = Chapters.query.filter_by(book_id=id)
    return render_template('chapters.html', id=id, chapters=chapters)

@main_bp.route('/article/<string:id>/<string:chapter_number>')
@login_required
def chapters(id,chapter_number):
    '''db = MysqlUtil()
    sql = "select content from chapters where bookid = '%s',chapter_number = '%s'".format(id, chapter_number)'''

    #content = db.fetchall(sql)
    content = Chapters.query.filter_by(book_id=id,chapter_number=chapter_number).first()
    if session.get('email'):
        user_email = session['email']
        history_entry = History(user_email=user_email,book_id=id,chapter_id=chapter_number)
        db.session.add(history_entry)
        db.session.commit()
    return render_template('article.html',content=content)
