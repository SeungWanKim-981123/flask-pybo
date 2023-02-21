from flask import Blueprint,render_template,request,url_for,g,flash
from werkzeug.utils import redirect
#본 파일에서 질문 class와 연관된 라우팅 함수들을 모조리 정의해줄 것임.
from pybo.models import Question,Answer,User
from pybo.forms import QuestionForm, AnswerForm
from .. import db
from datetime import datetime
bp=Blueprint('question',__name__,url_prefix='/question')

from pybo.views.auth_views import  login_required


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    return render_template('/question/question_detail.html',question=question,form=form)

@bp.route('/create/',methods=('GET','POST'))
@login_required
def create():#새로운 질문을 만들어주는 함수이므로 그것을 입력 받을 폼이 필요하다. 이래서 forms.py에서 Questionform 클래스를 끌어온 것이다.
    form=QuestionForm()#본 create 함수는 해당 url이 두가지 행위로부터 유입되므로 if문을 통해서 GET 요청인지 POST 요청인지를 구별한다.
    if request.method=="POST" and form.validate_on_submit():
        question=Question(subject=form.subject.data,content=form.content.data,create_date=datetime.now(),user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))#main별칭의 index함수로 가자. question의 리스트 항목으로 갈 수 있음.
    return render_template('question/question_form.html',form=form)
@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required#일단 로그인 조건이 충족되어야 돌아가는 함수라는 것임.
def modify(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user!=question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail',question_id=question_id))
    if request.method=='POST':
        form=QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)#form에 존재하는 데이터를 question 객체에 업데이트 진행을 해주고
            question.modify_date=datetime.now()#수정 시각을 따로 바꿔준다.
            db.session.commit()
            return redirect(url_for('question.detail',question_id=question_id))
    else:
        form=QuestionForm(obj=question)
    return render_template('question/question_form.html',form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user!=question.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))\

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question=Question.query.get_or_404(question_id)
    if g.user==_question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id))

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)