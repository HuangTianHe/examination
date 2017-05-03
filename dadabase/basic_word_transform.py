#coding=utf-8

#coding=utf-8
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicWordTranceform(Base):
    # 表的名字:
    __tablename__ = 'basic_word_transform'
    #通过页面上转换一栏获取数据

    #主键
    id=Column(Integer,primary_key=True)
    #0-复数形式，1-第三人称单数-plural；2-现在分词-ing；3-过去分词，过去式-past；4-比较级；5-最高级
    type=Column(Integer)
    #对应 basic_word_property.id 字段
    prop_id=Column(Integer)
    #转换格式的单词拼写
    spell=Column(String(255))
    #0-Disabled,  1-Enabled
    status=Column(Integer)