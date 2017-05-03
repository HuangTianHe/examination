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
    id=Column(Integer,primary_key=True)
    #对应 basic_word_property.id 字段
    prop_id=Column(Integer,primary_key=True)
    #音标书写
    spell=Column(String(255))
    #对应 basic_material.id 字段，发音的音频文件
    audio_file_md5=Column(String(128))
    #0 - 美式发音，1 - 英式发音
    type=Column(Integer)
