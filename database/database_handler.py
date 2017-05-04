#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import json
import re
import traceback
import copy


from sqlalchemy import Column, String, create_engine,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship

from database.basic_word_base import BasicWordBase
from database.basic_word_property import BasicWordProperty
from database.basic_word_phonetic import BasicWordPhonetic
from database.basic_material import BasicMaterail
from database.basic_word_sentence import BasicWordSentence
from database.basic_word_association import BasicWordAssociation
from database.basic_word_transform import BasicWordTranceform
from utils.mylogger import get_log
from examination import settings

engine = create_engine('mysql://admintest:dsjw2015@172.18.4.81:3307/word?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def handle_exception(fun):
    def inner_fun(*args,**kwargs):
        try:
            return  fun(*args,**kwargs)
        except Exception,e:
            t,b,tb=sys.exc_info()
            get_log(settings.LOG_NAME_BINGWORD).error( '%s:%s,%s'%(t,b,traceback.print_tb(tb)))
    return inner_fun

@handle_exception
def insert_basic_word_base(item):
    # 创建session对象:
    ob=BasicWordBase()
    ob.spell=item['en_word'].strip()
    #ob.desc=json.dumps(item['cn_meaning'],encoding='utf-8',ensure_ascii=False)
    ob.desc = json.dumps(item['desc'], encoding='utf-8', ensure_ascii=False)
    ob.type=1
    ob.status=1
    ob.upload_time=datetime.datetime.now()
    ob.update_time=datetime.datetime.now()
    id=save_data(ob)
    return id

@handle_exception
def insert_one_basic_word_property(basic_id,attribute,translation):
    ob=BasicWordProperty()
    ob.base_id=basic_id
    ob.type=0
    ob.attribute=attribute
    ob.translation=translation
    #ob.source_id=0
    ob.status=1
    ob.upload_time=datetime.datetime.now()
    ob.update_time=datetime.datetime.now()
    id=save_data(ob)
    return id

def insert_basic_word_properties(basic_id,material_ids,item):
    for attribute,translations in item['desc'].items():
        translations=translations.encode('utf-8')
        translations=translations.split(u'；')
        if not translations:
            translations = translations.split('；')
        for translation in translations:
            prop_id=insert_one_basic_word_property(basic_id,attribute,translation)
            insert_basic_word_phonetic(prop_id,material_ids,item)

@handle_exception
def insert_basic_word_phonetic(prop_id,material_ids,item):

    ob_us=BasicWordPhonetic()
    ob_us.prop_id=prop_id
    ob_us.spell=item['audio_us_href']
    ob_us.audio_file_md5=material_ids[0]
    ob_us.type=0
    save_data(ob_us)


    ob_uk = BasicWordPhonetic()
    ob_uk.prop_id = prop_id
    ob_uk.spell = item['audio_href']
    ob_uk.audio_file_md5 =material_ids[1]
    ob_uk.type = 1
    save_data(ob_uk)

@handle_exception
def insert_basic_material(item):
    ids=[]
    for audio in (item['audio_us'],item['audio']):
        regext=re.compile("(https://.*?)',",re.S)
        url=regext.findall(audio)
        url=url[0]
        print url
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
        session = DBSession()
        query=session.query(BasicMaterail).filter_by(md5sum=url).first()
        if query:
            ids.append(query.id)
        else:
            id=save_data(ob)
            ids.append(id)
    return ids

def insert_basic_word_transform(item):
    for i in range(len(item['tense_names'])):
        ob = BasicWordTranceform()
        ob.prop_ext=item['en_word'].strip()
        # 复数
        if item['tense_names'][i].strip() == 'Plural Form：':
            ob.type = 0
            ob.prop_id = 0
            ob.spell = item['tense_words'][i]
            ob.status = 0
        #第三人称单数
        elif item['tense_names'][i].strip()=='Simple Present：':
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
            get_log(settings.LOG_NAME_BINGWORD).error('the nonsupport transform type. '
                'type is %s,spell is %s'%(item['tense_names'][i],item['tense_words'][i]))

        save_data(ob)

def save_sentence(item):
    en_word=item['en_word']
    word=item['eg_sentence']['word']
    for i in range(len(item['eg_sentence']['cn_list'])):
        slist_cn=item['eg_sentence']['cn_list'][i]
        sentence_cn =''.join(slist_cn)
        slist_en =item['eg_sentence']['en_list'][i]
        sentence_en=''.join(slist_en)
        ob = BasicWordSentence()
        ob.prop_id=0
        ob.prop_ext='%s&%s'%(en_word,word)
        ob.index=i
        ob.english=sentence_en
        ob.chinese=sentence_cn
        ob.status=0
        save_data(ob)

def save_basic_word_association(master_id,item):
    # 词组
    for i in range(len(item['phrase_nature'])):
        for one in item['phrase_words'][i]:
            ob=BasicWordAssociation()
            ob.type=0
            ob.master_base_id=master_id
            ob.status=0
            ob.master_prop_id=0
            ob.slave_spell=one.strip()
            session = DBSession()
            slave=session.query(BasicWordBase).filter_by(spell=one.strip()).first()
            if slave:
                ob.slave_base_id=slave.id
            else:
                ob.slave_base_id=0
            save_data(ob)
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
            save_data(ob)

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
            save_data(ob)


def query_basiec_word_base(word):
    session = DBSession()
    query = session.query(BasicWordBase).filter_by(spell=word).first()
    if query:
        return True
    else:
        return False

def save_data(ob,try_time=1):
    try:
        # 创建session对象:
        session = DBSession()
        session.add(ob)
        session.commit()
        id=ob.id
        session.close()
        return id
    except:
        t, b, tb = sys.exc_info()
        get_log(settings.LOG_NAME_BINGWORD).error('save data appear error,try time is %s, %s:%s,%s' % (try_time,t, b, traceback.print_tb(tb)))
        if try_time>=settings.TRY_TIME:
            ob_data=copy.deepcopy(ob)
            if '_sa_instance_state' in ob_data:
                del ob_data['_sa_instance_state']
            get_log(settings.LOG_NAME_BINGWORD).error('save fail,want to save data is :%s'%(json.dumps(ob_data,encoding='utf-8',ensure_ascii=False)))
            return
        save_data(ob,try_time+1)