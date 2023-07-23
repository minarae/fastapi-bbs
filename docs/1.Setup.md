# 초기화
본 코드는 python 3.9 환경에서 구성되었다.
## 프로젝트 생성
프로젝트는 다음 코드로 생성한다.
``` shell
poetry new fastapi-bbs
```
위의 명령어를 입력하면 fastapi-bbs라는 디렉토리가 생성된다.
poetry 라이브러리를 통해서 파이썬 패키지 의존성을 관리하도록 할 것이다.
***
이제 디렉토리 이름을 변경한다. 처음에 poetry 명령어로 디렉토리를 생성하면 하위에 같은 이름으로 디렉토리가 더 생성된다
여기서는 fastapi-bbs로 생성하였기 때문에 fastapi-bbs 디렉토리 아래 fastapi-bbs라는 디렉토리가 생성된다.
이 디렉토리 이름을 app으로 변경한다.
그럼 디렉토리 구조가 아래와 같다.
```
fastapi-bbs
|- app
| |- __init__.py
|- tests
| |- __init__.py
|- poetry.lock
|- pyproject.toml
|- README.md

```
## 소스코드 클론
이제 코드를 가져오자. 이 프로젝트의 기본이 되는 코드는 아래 Repository이다.
<https://github.com/pahkey/fastapi-book>
해당 프로젝트는 fastapi 기반의 Backend에 Svelte 기반의 Frontend를 얻어서 개발한 프로젝트이다.
우선 적당한 위치에서 해당 Repository를 클론한다.
``` shell
git clone git@github.com:pahkey/fastapi-book.git
```
clone으로 가져온 코드를 지금 생성한 프로젝트 내에 적당한 위치로 복사하여서 이동한다.
기존 디렉토리에서 이 프로젝트 내에 어떤 위치로 이동할 것인지 아래 표로 정리한다.
| 기존 위치 | 이동할 위치 |
|:---:|:---:|
| domain | app/domain |
| frontend | frontend |
| .gitignore | .gitignore |
| main.py | app/main.py |
|database.py|database.py|
|models.py|models.py|
이 표에서 정리한 파일 이외의 파일은 복사하지 않고 새로 생성하여서 사용한다.
``` shell
cd fastapi-book
cp -R domain ../fastapi-bbs/app/
cp -R frontend ../fastapi-bbs/
cp .gitignore ../fastapi-bbs/
cp main.py ../fastapi-bbs/app/
cp database.py ../fastapi-bbs/
cp models.py ../fastapi-bbs/
```
이제 기본이 되는 코드는 가져온 셈이다.
## 의존성 패키지 설치
여기서 이제 프로젝트 디렉토리로 이동해서 사용할 패키지들을 설치한다.
### python
다음의 명령어를 통해서 fastapi-bbs 디렉토리로 이동하고 프로젝트에 필요한 패키지를 설치한다.
``` shell
cd fastapi-bbs
poetry add fastapi sqlalchemy "uvicorn[standard]" # 웹 서버 구동에 기본이 되는 패키지
poetry add pymysql alembic "pydantic[email]=^1.10.9" python-multipart aiomysql passlib bcrypt "python-jose[cryptography]" # 가져올 프로젝트 코드에서 사용할 패키지 리스트
```
### svelte
이번에는 frontend에서 사용할 node용 패키지를 설치한다.
여기서는 node 자체를 설치하는 방법은 생략한다.
``` shell
cd frontend
npm install
```
node에서 필요한 패키지에 대해서는 구동할 수 있도록 정리가 잘 되어 있어서 그대로 사용하면 된다.

## config
이제 설정 파일을 생성한다. 설정 파일은 .env로 생성할 것인데 이 프로젝트에서는 config 디렉토리를 생성하고 그 아래에 설정 파일을 두도록 할 것이다.
이렇게 하는 이유는 본 코드를 이후에 도커를 통해서 배포 및 운영하는데 배포할 때마다 설정 파일을 생성하기 보다 호스트에서 config 디렉토리를 관리하고 도커에서는 해당 디렉토리를 공유하는 방식으로 운영을 할 예정이기 때문이다.
이 프로젝트에서 우선 사용할 .env 항목은 다음과 같다.
```
ACCESS_TOKEN_EXPIRE_MINUTES=60
SECRET_KEY=xxxxxxxxxxxxxx
DB_USER=test
DB_PW=database_password
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=fastapi_book
```
이 프로젝트에서는 Database를 mysql로 사용한다. 원래 가져온 코드에서는 DB를 sqlite로 사용하였으나 장기적으로 DB를 운영하기에는 mysql이 더 적합해보이기 때문에 mysql를 사용하기로 한다.
위와 같이 접속 정보를 입력하고 저장한다.
다시 말하지만 .env의 경로는 **config/.env**이다.
***
config 파일을 생성하였으니 config 파일을 읽어오는 코드에서 경로를 변경해주어야 한다.
**app/domain/user/user_router.py** 파일에서 로그인에 필요한 정보를 가져오기 위해서 config 파일을 읽어온다.
이 파일을 열어서  15 라인을 다음과 같이 수정한다.
``` python
config = Config('config/./env')
```
이렇게 코드를 수정하면 위에서 설정한 .env 파일의 내용을 가져올 수 있다.
## Database 연결
위에서 DB는 mysql을 사용한다고 하였고 설정 파일에서 DB에 접속하기 위한 내용을 추가하였다.
복사해온 코드에서는 언급한 바와 같이 sqlite를 사용하기 때문에 DB와 관련된 내용은 다소 수정을 하여야 한다.
그 중에서 **database.py** 파일은 DB에 접속하기 위한 코드가 있는데 이 내용으로 교체한다.
``` python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from starlette.config import Config

config = Config('config/.env')
DB_USER = config('DB_USER')
DB_PW = config('DB_PW')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_DATABASE = config('DB_DATABASE')

ASYNC_DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8"

# SQLAlchemy 엔진 생성
engine = create_engine(DB_URL)
async_engine = create_async_engine(ASYNC_DB_URL, echo=True, pool_pre_ping=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# 의존성 함수로 사용할 get_db 함수 정의
def get_db() -> Session:
    try:
        # 세션 생성
        db = session()
        # 생성한 세션을 제공
        yield db
    finally:
        # 세션 종료
        db.close()

async def get_async_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

```
DB에 접속하는 함수를 두 가지로 작성하였다. 하나는 동기 방식이고 다른 하나는 비동기 방식이다.
기존의 게시판 코드가 이렇게 두 가지로 되어있기 때문에 우선 여기서도 두 가지로 작성하여서 사용한다.
추후에는 DB를 사용하는 코드는 모두 비동기로 동작하도록 바꿀 것이다.
하지만 초기 설정에서는 일단 코드가 동작되게 하는데 초점을 두고 있기 때문에 두 개의 함수로 구성하도록 한다.

## python 코드 호환성 수정
마지막으로 python에서 사용하는 코드의 호환성을 맞추기 위해서 코드를 약간 수정하여야 한다.
처음에 언급한 것과 같이 해당 코드는 python 3.9에서 개발하는데 복사해온 코드는 python 3.10 에서 작성하여서 3.9에서 사용할 수 없는 문법이 있다.

python 3.10에서는 schema를 선언할 때 | 를 사용할 수 있는데 3.9에서는 허용하지 않는다.
app/domain/answer/answer_shcema.py를 열어보면 다음과 같이 작성되어 있다.
``` python
...
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

    class Config:
        orm_mode = True
...
```

여기서 |를 사용하는 문법은 3.9에서 사용할 수 없기 때문에 다음과 같이 수정한다.

``` python
# 생략
from typing import Optional

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: Optional[User]
    question_id: int
    modify_date: Optional[datetime.datetime] = None
    voter: list[User] = []

    class Config:
        orm_mode = True
# 생략
```
이렇게 작성하면 3.9에서 정상작동하게 된다.
**app/domain/question/question_schema.py**도 수정해준다.
``` python
# 생략
from typing import Optional

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: Optional[User]
    modify_date: Optional[datetime.datetime] = None
    voter: list[User] = []

    class Config:
        orm_mode = True
# 생략
```

***
이제 서비스를 정상적으로 구동하기 위한 준비가 마무리 되었다.
하지만 서비스가 올라오기만 할 뿐 아직 테이블 생성을 하지 않았기 때문에 어떤 동작도 하지 않는다.
DatabaseSetup 에서 테이블에 관련된 내용을 정리한다.
