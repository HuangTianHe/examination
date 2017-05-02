#coding=utf-8

#coding=utf-8
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicWordSentence(Base):
    # 表的名字:
    __tablename__ = 'basic_word_sentence'

    #主键
    id=Column(Integer)
    #对应 basic_word_property.id 字段
    prop_id=Column(Integer)
    #句子索引
    index=Column(Integer)
    #英文句子
    english=Column(Text)
    #句子中文翻译
    chinese=Column(Text)
    #0-Disabled,  1-Enabled
    status=Column(Integer)
