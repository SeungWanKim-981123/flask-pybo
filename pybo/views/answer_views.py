#답변 라우팅 함수들을 관리하는 라우팅 함수에 해당한다
from datetime import  datetime

from flask import Blueprint,url_for,request,render_template,g,flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question,Answer
bp=Blueprint('answer',__name__,url_prefix='/answer')

from .auth_views import login_required
@bp.route('/create/<int:question_id>',methods=('POST',))
@login_required
def create(question_id):#답변을 db에 기록하는 기능의 함수를 의미한다.
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']#request 객체의 속성을 딕셔너리 형태로 가지고 있음.
        answer = Answer(content=content, create_date=datetime.now(),user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id),answer.id))
    return render_template('question/question_detail.html',question=question,form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=answer.question.id),answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    question_id=answer.question.id
    if g.user!=answer.user:
        flash('삭제 권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id))

@bp.route('/vote/<int:answer_id>')
@login_required
def vote(answer_id):
    _answer=Answer.query.get_or_404(answer_id)
    if g.user==_answer.user:
        flash('본인이 작성한 글은 추천할 수 없습니다.')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=_answer.question.id))