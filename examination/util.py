#coding:utf8#
from bingitems import *
import json

def bing_item_output(item):
    print "单词"
    print item['en_word']
    print "US音标"
    print item['audio_us']
    print item['audio_us_href']
    print "音标"
    print item['audio']
    print item['audio_href']
    print '词性'
    #print item['natures']
    print '|'.join(item['natures'])
    print '|'.join(item['natures_meaning'])
    print '时态'
    print '|'.join(item['tense_names'])
    print '|'.join(item['tense_words'])

    print '词组'
    print '|'.join(item['phrase_nature'])
    print ([ '|'.join(i) for i in item['phrase_words'] if i])

    print '同义词'
    print '|'.join(item['synonymous_nature'])
    print ([ '|'.join(i) for i in item['synonymous_words'] if i])

    print '反义词'
    print '|'.join(item['antonym_nature'])
    print ([ '|'.join(i) for i in item['antonym_words'] if i])

    print '英英翻译'
    #print item['en2en_explain_nature']
    #print item['en2en_explain_sentence']

    print '|'.join(item['en2en_explain_nature'])
    print '|'.join(item['en2en_explain_sentence'])

    print '中文含义'
    #print item['cn_meaning']
    print '|'.join(item['cn_meaning'])

def bing_sen_output(item):
    #print json.dumps(item['en_word'] , indent=2, ensure_ascii=False)
    #print json.dumps(item['eg_sentence'] , indent=2, ensure_ascii=False)

    for slist in item['eg_sentence']['cn_list']:
        #for  i in slist:
        print ''.join(slist)
    for slist in item['eg_sentence']['en_list']:
        #for  i in slist:
        print ''.join(slist)

    '''
    print '例句'
    print item['en_word']
    print item['eg_sentence']
    '''
def exam_item_output(item):
    print '学段'
    print item['stage']
    print '学科'
    print item['subject']
    print item['ttype']
    print '学年'
    print item['year']
    print '试卷类型'
    print item['exam_type']
    print '试卷子类型'
    print item['exam_child_type']
    print item['list_href']
    
    print '试卷名称'
    print item['paper_text']
    print '试卷href'
    print item['paper_href']
    print '更新时间'
    print item['update_time']
    print 'view count'
    print item['view_count']
    print '下载次数'
    print item['download_count']



def paper_item_output(item):

    print '试卷href'
    print item['paper_href']
    print '试卷名称'
    print item['paper_name']
    print '总分'
    print item['total_score']
    print '难度'
    print item['diffcult']
    print 'view count'
    print item['view']
    print 'download count'
    print item['download']
    print '试卷结构'
    print json.dumps(item['lstruct'], indent=2,ensure_ascii=False)
    

