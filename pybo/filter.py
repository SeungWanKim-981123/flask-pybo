#본 파일은 템플릿에 필터를 적용하기 위해서 작성해놓는 것이고 다른 html 문서들에서 이를 활용한다고 보면 된다.
def format_datetime(value,fmt='%Y년 %m월 %d일  %p %I : %M'):
    return value.strftime(fmt) # 전달받은 datetime 객체를 포맷화시켜 돌려주는 함수에 해당한다. 다른 곳에서 이 함수를 써먹을 예정임.
