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
