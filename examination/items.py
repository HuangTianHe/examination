# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExaminationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stage = scrapy.Field() 
    subject = scrapy.Field() 
    ttype = scrapy.Field() 
    year = scrapy.Field() 
    exam_type = scrapy.Field() 
    exam_child_type = scrapy.Field()
    list_href = scrapy.Field()
    
    paper_text = scrapy.Field()
    paper_href = scrapy.Field()
    update_time = scrapy.Field()
    view_count = scrapy.Field()
    download_count = scrapy.Field()

class PaperinationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    paper_href = scrapy.Field()
    paper_name = scrapy.Field() 
    total_score = scrapy.Field() 
    diffcult = scrapy.Field() 
    view = scrapy.Field()
    download = scrapy.Field()
    lstruct = scrapy.Field() 

class QuestionItem(scrapy.Item):
    question_href = scrapy.Field()
    body = scrapy.Field() 
    score = scrapy.Field() 
    answer = scrapy.Field() 
    qtype = scrapy.Field() 
    analiys = scrapy.Field() 
    
