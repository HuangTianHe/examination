#coding=utf-8
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicWordBase(Base):
    # 表的名字:
    __tablename__ = 'basic_word_base'
    #用于存储页面中最上方【单词】，【发音】，【翻译描述】三部分数据

    #主键ID
    id=Column(Integer,primary_key=True)
    #单词拼写
    spell=Column(String(20))
    #单词的详细解释
    desc=Column(Text)
    #类型：1-单词，2-词组
    type=Column(Integer)
    #0-Disabled, 1-Enabled
    status=Column(Integer)
    #单词首次入库时间
    upload_time=Column(DateTime)
    #单词最后更新时间
    update_time=Column(DateTime)
