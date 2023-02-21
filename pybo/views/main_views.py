from flask import Blueprint,url_for

from werkzeug.utils import redirect
bp=Blueprint('main',__name__,url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))#그냥 루트 링크로 접속함녀 url_for함수가 url을 반환하고 거기로 이동.

