from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user.id'), primary_key=True),
    Column('question_id', INTEGER(unsigned=True), ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user.id'), primary_key=True),
    Column('answer_id', INTEGER(unsigned=True), ForeignKey('answer.id'), primary_key=True)
)


class Question(Base):
    __tablename__ = "question"

    id = Column(INTEGER(unsigned=True), primary_key=True)
    subject = Column(String(length=255), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=question_voter, backref='question_voters')


class Answer(Base):
    __tablename__ = "answer"

    id = Column(INTEGER(unsigned=True), primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(INTEGER(unsigned=True), ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    user_id = Column(INTEGER(unsigned=True), ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')


class User(Base):
    __tablename__ = "user"

    id = Column(INTEGER(unsigned=True), primary_key=True)
    username = Column(String(length=30), unique=True, nullable=False)
    password = Column(String(length=100), nullable=False)
    email = Column(String(length=150), unique=True, nullable=False)
