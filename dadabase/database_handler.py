#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import json
import re

from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship

from dadabase.basic_word_base import BasicWordBase
from dadabase.basic_word_property import BasicWordProperty
from dadabase.basic_word_phonetic import BasicWordPhonetic
from dadabase.basic_material import BasicMaterail
from dadabase.basic_word_sentence import BasicWordSentence
from dadabase.basic_word_association import BasicWordAssociation
from dadabase.basic_word_transform import BasicWordTranceform
from dadabase import  ssdb_handler

engine = create_engine('mysql://admintest:dsjw2015@172.18.4.81:3307/word?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def insert_basic_word_base(item):
    # 创建session对象:
    session = DBSession()
    ob=BasicWordBase()
    ob.spell=item['en_word'].strip()
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
    return ob.id

def insert_basic_word_properties(basic_id,material_ids,item):
    for attribute,translations in item['desc'].items():
        translations=translations.encode('utf-8')
        translations=translations.split(u'；')
        if not translations:
            translations = translations.split('；')
        for translation in translations:
            prop_id=insert_one_basic_word_property(basic_id,attribute,translation)
            insert_basic_word_phonetic(prop_id,material_ids,item)

def insert_basic_word_phonetic(prop_id,material_ids,item):

    # 创建session对象:
    session = DBSession()
    ob=BasicWordPhonetic()
    ob.prop_id=prop_id
    ob.spell=item['audio_us_href']
    ob.audio_file_md5=material_ids[0]
    ob.type=0
    session.add(ob)
    session.commit()

    # 创建session对象:
    session = DBSession()
    ob = BasicWordPhonetic()
    ob.prop_id = prop_id
    ob.spell = item['audio_href']
    ob.audio_file_md5 =material_ids[1]
    ob.type = 1
    session.add(ob)
    session.commit()

def insert_basic_material(item):
    ids=[]
    for audio in (item['audio_us'],item['audio']):
        regext=re.compile('(https://.*?,)',re.S)
        url=regext.findall(audio)
        url=url[0]
        print url
        session=DBSession()
        ob=BasicMaterail()
        ob.md5sum=url
        ob.img_url=''
        ob.local_ip=''
        ob.local_path=''
        ob.fdfs_group_name=''
        ob.fdfs_storage_ip=''
        ob.fdfs_remote_file_id=''
        ob.fdfs_size='0'
        ob.upload_time=datetime.datetime.now()
        ob.update_time=datetime.datetime.now()
        session.add(ob)
        session.commit()
        ids.append(ob.id)
    return ids

def insert_basic_word_transform(item):
    for i in range(len(item['tense_names'])):
        vaule=item['tense_words'][i]
        session = DBSession()
        ob = BasicWordTranceform()
        #第三人称单数
        if item['tense_names'][i].strip()=='Simple Present：':
            ob.type=1
            ob.prop_id=0
            ob.spell=item['tense_words'][i]
            ob.status=0
        #现在分词-ing
        elif item['tense_names'][i].strip()=='Present Participle：':
            ob.type=2
            ob.prop_id=0
            ob.spell=item['tense_words'][i]
            ob.status=0
        #过去式-past
        elif item['tense_names'][i].strip()=='Past Tense：':
            ob.type=3
            ob.prop_id=0
            ob.spell=item['tense_words'][i]
            ob.status=0
        #比较级
        elif item['tense_names'][i].strip()=='Comparative Degree：':
            ob.type=4
            ob.prop_id=0
            ob.spell=item['tense_words'][i]
            ob.status=0
        #最高级
        elif item['tense_names'][i].strip()=='Superlative：':
            ob.type=5
            ob.prop_id=0
            ob.spell=item['tense_words'][i]
            ob.status=0
        else:
            print item['tense_names'][i]
            print item['tense_words'][i]




        session.add(ob)
        session.commit()

def save_sentence(item):
    en_word=item['en_word']
    word=item['eg_sentence']['word']
    for i in range(len(item['eg_sentence']['cn_list'])):
        slist_cn=item['eg_sentence']['cn_list'][i]
        sentence_cn =''.join(slist_cn)
        slist_en =item['eg_sentence']['en_list'][i]
        sentence_en=''.join(slist_en)
        session = DBSession()
        ob = BasicWordSentence()
        ob.prop_id=0
        ob.prop_ext='%s&%s'%(en_word,word)
        ob.index=i
        ob.english=sentence_en
        ob.chinese=sentence_cn
        ob.status=0
        session.add(ob)
        session.commit()

def save_basic_word_association(master_id,item):
    # 词组
    for i in range(len(item['phrase_nature'])):
        for one in item['phrase_words'][i]:
            session=DBSession()
            ob=BasicWordAssociation()
            ob.type=0
            ob.master_base_id=master_id
            ob.status=0
            ob.master_prop_id=0
            ob.slave_spell=one.strip()
            slave=session.query(BasicWordBase).filter_by(spell=one.strip()).first()
            if slave:
                ob.slave_base_id=slave.id
            else:
                ob.slave_base_id=0
            session.add(ob)
            session.commit()
    #近义词
    for i in range(len(item['synonymous_nature'])):
        for one in item['synonymous_words'][i]:
            session=DBSession()
            ob=BasicWordAssociation()
            ob.type=1
            ob.master_base_id=master_id
            ob.status=0
            ob.master_prop_id = 0
            ob.slave_spell = one.strip()
            slave = session.query(BasicWordBase).filter_by(spell=one.strip()).first()
            if slave:
                ob.slave_base_id=slave.id
            else:
                ob.slave_base_id=0
            session.add(ob)
            session.commit()

    #反义词
    for i in range(len(item['antonym_nature'])):
        for one in item['antonym_words'][i]:
            session=DBSession()
            ob=BasicWordAssociation()
            ob.type=2
            ob.master_base_id=master_id
            ob.status=0
            ob.master_prop_id = 0
            ob.slave_spell = one.strip()
            slave = session.query(BasicWordBase).filter_by(spell=one.strip()).first()
            if slave:
                ob.slave_base_id=slave.id
            else:
                ob.slave_base_id=0
            session.add(ob)
            session.commit()






    # 近义词
    synonym = []
    # 反义词
    antonym = []

def save_ssdb(master_id,item):
    ssdb_kay='ssdb_word_%s'%(item['en_word'])
    transform={}

    association={}
