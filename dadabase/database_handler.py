#coding=utf-8

import datetime

from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship

from dadabase.basic_word_base import BasicWordBase

engine = create_engine('mysql://admintest:dsjw2015@172.18.4.81:3307/test_hth')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def insert_basic_word_base(item):
    # 创建session对象:
    session = DBSession()
    ob=BasicWordBase()
    ob.spell=item['en_word']
    ob.desc=item['cn_meaning']
    ob.status=1
    ob.upload_time=datetime.datetime.now()
    ob.update_time=datetime.datetime.now()
    session.add(ob)
    session.commit()
    print ob.id
    return ob.id

