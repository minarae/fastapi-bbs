from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ...domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    password = pwd_context.hash(user_create.password1)
    print(len(password), password)
    db_user = User(username=user_create.username,
                   password=password,
                   email=user_create.email)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
