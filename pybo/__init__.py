from flask import Flask,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown
naming_convention={
	"ix":'ix_%(column_0_label)s',
	"uq":"uq_%(table_name)s_%(column_0_name)s",
	"ck":"ck_%(table_name)s_%(column_0_name)s",
	"fk":"fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
	"pk":"pk_%(table_name)s"
}
db=SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate=Migrate()


def page_not_found(e):
	return render_template('404.html'),404

def create_app():
	app=Flask(__name__)
	app.config.from_envvar('APP_CONFIG_FILE')

	#ORM
	db.init_app(app)
	if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
		migrate.init_app(app,db,render_as_batch=True)
	else:
		migrate.init_app(app,db)
	from . import models #테이블을 나타내는 클래스들을 끌어오려는 것임.

	#블루포인트(라우팅 함수를 관리하는 것임)
	from .views import main_views,question_views,answer_views,auth_views
	app.register_blueprint(main_views.bp)
	app.register_blueprint(question_views.bp)
	app.register_blueprint(answer_views.bp)
	app.register_blueprint(auth_views.bp)

	#필터
	from .filter import format_datetime
	app.jinja_env.filters['datetime']=format_datetime#이것은 필터를 등록해준 것에 해당한다.
	#jinja 엔진의 환경에 필터로 연결해준 필터명은 datetime에 해당함을 알 수 있다.

	#Markdown
	Markdown(app,extensions=['nl2br','fenced_code'])#마크 다운 문법을 사용하는데 줄바꿈을 편하게 할 수 있는(br) ml2br과 코드를 표시할 수 있는 fenced_code를 익스텐션으로 추가함.

	#오류 페이지
	app.register_error_handler(404,page_not_found)
	return app
