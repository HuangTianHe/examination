# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from utils.mylogger import get_log
from examination import  settings

class ExaminationPipeline(object):
    def process_item(self, item, spider):
        get_log(settings.LOG_NAME_BINGWORD).warning(json.dumps(dict(item),ensure_ascii=False,encoding='utf-8'))
        return item
