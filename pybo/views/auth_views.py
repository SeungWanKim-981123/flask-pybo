#본 파이썬 파일은 로그인과 로그 아웃에 대한 함수를 라우팅하는 코드가 담겨있다.
from flask import Blueprint,url_for,render_template,flash,request,session,g
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm,UserLoginForm
from pybo.models import User

import functools#login_required 함수를 데코레이터를 만들어주기 위해서 필요한 것임.
bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/signup/',methods=('GET','POST'))
def signup():#회원가입의 기능을 하는 함수를 의미한다.
    form=UserCreateForm()
    if request.method=='POST' and form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()#user가 일단 있는지 없는지를 검사한다.
        if not user:#유저가 기존의 db에 없는 경우 --> 새로 유저를 등록하는 것이 맞다.
            user=User(username=form.username.data,password=generate_password_hash(form.password1.data),email=form.email.data)
            #폼으로부터 데이터를 읽어들이는 코드에 해당한다.
            db.session.add(user)
            db.session.commit()
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html',form=form)

@bp.route('/login/',methods=('GET','POST'))
def login():
    form=UserLoginForm()
    if request.method=='POST' and form.validate_on_submit():
        error=None
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            error="존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password,form.password.data):
            error="비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()#플라스크에서 제공하는 세션임. 쿠키 이런거라고 보면 됨 ㅇㅇㅇ 일종의 객체임.
            session['user_id']=user.id
            _next=request.args.get('next','')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
            return redirect(url_for('main.index'))#여기에서 질문 리스트 화면으로 가면서 함수가 종료됨.
        flash(error)
    return render_template('auth/login.html',form=form)#GET요청인 경우에는 로그인 화면을 보여준다.

@bp.before_app_request #이 데코레이션은 어떠한 라우팅 함수보다도 먼저 실행되어야함을 나타낸다.
def load_logged_in_user():
    user_id=session.get('user_id')
    if user_id is None:#user의 id값이 존재하지 않는 경우.
        g.user=None
    else:
        g.user=User.query.get(user_id)#g.user에는 User객체가 저장되므로 추후에 User의 아이디나 이메일을 알아내는 데에 유용하다.

@bp.route('/logout/')#로그아웃의 기능을 구현하는 함수임.
def logout():
    session.clear()#존재하는 세션을 지워버린다.
    return redirect(url_for('main.index'))

def login_required(view):#이건 추후에 데코레이팅 기능을 하는 데코레이터 함수에 해당한다.
    @functools.wraps(view)
    def wrapped_view(*args,**kwargs):
        if g.user is None:
            _next=request.url if request.method=='GET' else ''
            return redirect(url_for('auth.login',next=_next))
        return view(*args,**kwargs)
    return wrapped_view