#coding=utf-8

import pyssdb
from examination import settings

connection=None
ssdb_config=settings.SSDB_CONFIG

def connect(host=ssdb_config['host'],port=ssdb_config['port']):
    connection=pyssdb.Client(host,port)
    return connection

def save(conn,index,value):
    global connection
    if not connection:
        connection = connect()
    if not conn:
        conn=connection
    conn.set(index,value)

def get_value(conn,index):
    global connection
    if not connection:
        connection = connect()
    if not conn:
        conn=connection
    result=conn.get(index)
    return result

if __name__=="__main__":
    connecttion=connect()
    #save(connecttion,'test','test')
    #result=get_value('test')

    print get_value(connecttion,'ssdb_question_json_10.10.2.108_39017280')
    print get_value(connecttion, 'ssdb_question_html_10.10.2.108_39017280')
