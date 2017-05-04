#coding=utf-8

#coding=utf-8
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicWordProperty(Base):
    # 表的名字:
    __tablename__ = 'basic_word_property'
    #1.英汉翻译通过逐行并按分隔符分隔得到词性词义的翻译
    #2.英英翻译通过页面上【英英】一栏根据词性词义获取并保存

    #主键
    id=Column(Integer,primary_key=True)
    #对应 basic_word_base.id 字段
    base_id=Column(Integer)
    #0-英汉翻译；1-英英翻译
    type=Column(Integer)
    #词性标记。例如：n-名词，v-动词
    attribute=Column(String(16))
    #单词该词性的翻译
    translation=Column(String(255))
    #
    source_id=Column(Integer)
    #0-Disabled,  1-Enabled
    status=Column(Integer)
    #首次入库时间
    upload_time=Column(DateTime)
    #最后更新时间
    update_time=Column(DateTime)
