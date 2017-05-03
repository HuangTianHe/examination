#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import json

from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship

from dadabase.basic_word_base import BasicWordBase
from dadabase.basic_word_property import BasicWordProperty
from dadabase.basic_word_phonetic import BasicWordPhonetic

engine = create_engine('mysql://admintest:dsjw2015@172.18.4.81:3307/word?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def insert_basic_word_base(item):
    # 创建session对象:
    session = DBSession()
    ob=BasicWordBase()
    ob.spell=item['en_word']
    #ob.desc=json.dumps(item['cn_meaning'],encoding='utf-8',ensure_ascii=False)
    ob.desc = json.dumps(item['desc'], encoding='utf-8', ensure_ascii=False)
    ob.type=1
    ob.status=1
    ob.upload_time=datetime.datetime.now()
    ob.update_time=datetime.datetime.now()
    session.add(ob)
    session.commit()
    print ob.id
    return ob.id

def insert_one_basic_word_property(basic_id,attribute,translation):
    # 创建session对象:
    session = DBSession()
    ob=BasicWordProperty()
    ob.base_id=basic_id
    ob.type=0
    ob.attribute=attribute
    ob.translation=translation
    #ob.source_id=0
    ob.status=1
    ob.upload_time=datetime.datetime.now()
    ob.update_time=datetime.datetime.now()
    session.add(ob)
    session.commit()

def insert_basic_word_properties(basic_id,item):
    for attribute,translations in item['desc'].items():
        translations=translations.encode('utf-8')
        translations=translations.split(u'；')
        if not translations:
            translations = translations.split('；')
        for translation in translations:
            insert_one_basic_word_property(basic_id,attribute,translation)

def insert_basic_word_phonetic(prop_id,audio_file_md5,item):
    for type in (0,1):
        # 创建session对象:
        session = DBSession()
        ob=BasicWordPhonetic()
        ob.prop_id=prop_id
        ob.spell=item['audio_us_href']
        ob.audio_file_md5=item['audio_us']
        ob.type=type
        session.add(ob)
        session.commit()

def insert_basic_word_transform():
    pass

def save_sentence(item):
    pass