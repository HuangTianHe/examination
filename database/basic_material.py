#coding=utf-8
import datetime
from sqlalchemy import Column, String, create_engine,Integer,ForeignKey,Text,text,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

class BasicMaterail(Base):
    # 表的名字:
    __tablename__ = 'basic_material'
    id=Column(Integer,primary_key=True)
    md5sum=Column(String(255),default='')
    #上线的七牛地址
    img_url=Column(String(255))
    #存储到本地服务器 IP
    local_ip=Column(String(255))
    local_path=Column(String(512))
    fdfs_storage_ip=Column(String(255))
    fdfs_group_name=Column(String(255))
    fdfs_remote_file_id=Column(String(255))
    fdfs_size=Column(String(255),default='0')
    upload_time=Column(DateTime)
    update_time=Column(DateTime,default=datetime.datetime.now())
    status=Column(Integer,default=0)
