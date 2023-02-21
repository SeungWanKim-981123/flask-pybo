from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField,EmailField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class QuestionForm(FlaskForm):#FlaskForm을 상속받아서 QuestionForm을 만드는 것이다.
    subject=StringField('제목',validators=[DataRequired('제목은 필수입력 항목입니다.')])#얘는 String을 썼으니까 글자수 제한이 있고, 필수로 입력해야함.
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수입력 항목입니다.')])#얘는 Text를 썼으니까 글자수 제하이 없다, 필수로 입력할 필요는 없음.

class AnswerForm(FlaskForm):
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):#사용자로부터 회원가입을 받기 위한 폼의 클래스를 의미하며 이에 필요한 함수들은 헤더의 명령어로 모두 import 해주었음.
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    password1=PasswordField('비밀번호',validators=[DataRequired(),EqualTo('password2','비밀번호가 일치하지 않습니다.')])
    password2=PasswordField('비밀번호 확인',validators=[DataRequired()])
    email=EmailField('이메일',validators=[DataRequired(),Email()])

class UserLoginForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(),Length(min=3,max=25)])
    password=PasswordField('비밀번호',validators=[DataRequired()])