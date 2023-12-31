
from tkinter import CASCADE
from turtle import title
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key= True,nullable= False)
    title = Column(String,nullable= False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    user = Relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key= True,nullable= False)
    email = Column(String,nullable= False,unique=True)
    name = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    #post = Relationship("Post")
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    #user = Relationship("User")

