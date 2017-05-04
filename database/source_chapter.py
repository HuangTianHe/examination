#coding=utf-8

#coding=utf-8
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class SourceChapter(Base):
    # 表的名字:
    __tablename__ = 'source_chapter'

    #主键
    id=Column(Integer)
    #
    source_id=Column(Integer)
    #
    version=Column(String(128))
    #
    stage=Column(String(128))
    #
    directory=Column(String(128))
    #对应 neworiental_v3 库 entity_teaching_chapter.id 字段
    chapter=Column(String(128))
    #标记是否为章节重点单词：0-不是重点，1-是重点单词
    emphasis=Column(Integer)
    #是否为课标：0-不是课标，1-是课标
    course_standard=Column(Integer)
    #是否为中考单词：0-不是，1-是
    high_entrance=Column(Integer)
    #是否为高考单词：0-不是，1-是
    college_entrance=Column(Integer)
    #0-Disabled, 1-Enabled
    status=Column(Integer)