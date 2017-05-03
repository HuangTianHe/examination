#coding=utf-8

from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicWordAssociation(Base):
    # 表的名字:
    __tablename__ = 'basic_word_association'
    # 用于存储页面中【搭配】，【同义词】，【反义词】一栏数据


    # 表的结构:

    #主键id
    id = Column(Integer, primary_key=True)
    # 关联类型：0 - 词组 - phrase；1 - 近义词，同义词 - synonym；2 - 反义词 - antonym
    type=Column(Integer)
    #对应 basic_word_base.id 字段；【注意】这里的关联是单向的：单词 => 单词或词组
    master_base_id=Column(Integer)
    #主词关联的词性
    master_prop_id=Column(Integer)
    #对应 basic_word_base.id 字段
    slave_base_id=Column(Integer)
    #0-Disabled,  1-Enabled
    status=Column(Integer)
    slave_spell=Column(String(128))
