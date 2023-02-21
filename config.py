import os
BASE_DIR=os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS=False#데이터베이스를 어느 경로로 접근할 지, 수정사항은 적용할지를 나타내는 코드에 해당한다.
SECRET_KEY="dev"