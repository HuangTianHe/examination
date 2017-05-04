#coding=utf-8

#coding=utf-8
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicWordPhonetic(Base):
    # 表的名字:
    __tablename__ = 'basic_word_phonetic'

    #主键
    id=Column(Integer)
    #
    spell=Column(String(128))
    translation=Column(String(255))
    #0-Disabled, 1-Enabled
    status=Column(Integer)