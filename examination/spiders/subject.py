# -*- coding: utf-8 -*-
import scrapy
from  examination.items import ExaminationItem,PaperinationItem
import json
from examination.util import *



prefix = 'http://www.jyeoo.com'
class SubjectSpider(scrapy.Spider):
    name = "subject"
    allowed_domains = ["jyeoo.com"]
    start_urls = (
        #'http://www.jyeoo.com/math/report/',
        'http://www.jyeoo.com/math/report/search?pa=1',
    )

    def parse(self, response):
        
        item = ExaminationItem()
        #print "*"*100
        index =1 
        l =  response.xpath("/html/body/div[6]/div/ul/li[1]/ul/li")
        for s in l:
            ll = response.xpath("/html/body/div[6]/div/ul/li[1]/ul/li[%d]/div/a" % index)
            stage = response.xpath("/html/body/div[6]/div/ul/li[1]/ul/li[%d]/div/a" % index)
            stage_name_path = response.xpath("/html/body/div[6]/div/ul/li[1]/ul/li[%d]/span" % index)
            stage_name = stage_name_path.xpath('text()').extract()
            for i in ll:
                #print i.xpath('text()').extract()[0], stage_name[0], i.xpath('@href').extract()[0]
                subject_text = i.xpath('text()').extract()[0]
                stage_href = i.xpath('@href').extract()[0]
                stage_name_value = stage_name[0] 

                item['subject'] = subject_text
                item['stage'] = stage_name_value

                yield scrapy.Request(url=prefix+stage_href, meta={'item':item},callback=self.parse_type) 
 
            index = index + 1
        #print "*"*100
        return 

    def parse_type(self, response):
        
        item = response.meta['item']
        #print "="*100
        l = response.xpath('/html/body/div[6]/div/div[2]/a')
        index = 0 
        for t in l:
            index = index + 1 
            type_xpath = response.xpath( '/html/body/div[6]/div/div[2]/a[%d]' % index)
            type_href = type_xpath.xpath('@href').extract()
            type_text = type_xpath.xpath('text()').extract()
            type_href_value = type_href[0]
            type_text_value = type_text[0]
            item['ttype'] = type_text_value
            #print type_text[0], type_href[0]
            yield scrapy.Request(url=prefix+type_href_value, meta={'item':item},  callback=self.parse_year) 
            
        #print "="*100
        return 
      
    def parse_year(self, response):

        item = response.meta['item']
        #print "-"*100
        index = 0
        l = response.xpath('/html/body/div[6]/div/div[4]/a')
        for y in l:
            index = index + 1 
            year_xpath = response.xpath('/html/body/div[6]/div/div[4]/a[%d]' % index)
            year_href = year_xpath.xpath('@href').extract()
            year_text = year_xpath.xpath('text()').extract()

            year_href_value = year_href[0]
            year_text_value = year_text[0]

            item['year'] = year_text_value
            #print year_text_value, year_href_value
            yield scrapy.Request(url=prefix+year_href_value, meta={'item':item}, callback=self.parse_exam_type) 

        self.parse_exam_type(response)
        #print "-"*100
        return 

    def parse_exam_type(self, response):
        
        #print "%"*100
        index = 0
        l = response.xpath('//*[@id="divLeftMenuTree"]/li')
        item = response.meta['item']
        for tt in l:
            index = index + 1
            exam_xpath = response.xpath('//*[@id="divLeftMenuTree"]/li[%d]/a' % index)
            exam_href = exam_xpath.xpath('@href').extract()
            exam_text = exam_xpath.xpath('text()').extract()
            if exam_href and exam_text:
                #print index , exam_href[0], exam_text[0]
                exam_text_value = exam_text[0]
                exam_href_value = exam_href[0]
                item['exam_type'] = exam_text_value 
                item['list_href'] = prefix+exam_href_value 
            else:
                continue
            
            child_exam_xpath = response.xpath('//*[@id="divLeftMenuTree"]/li[%d]/ul/li' % index)
            k = 0 
            for cc in  child_exam_xpath:
                k = k+1
                child_xpath = response.xpath('//*[@id="divLeftMenuTree"]/li[%d]/ul/li[%d]/a' % (index, k))
                exam_href = child_xpath.xpath("@href").extract()
                exam_text = child_xpath.xpath("text()").extract()
                #print "    ", exam_href[0], exam_text[0]
                #exam_list.append(exam_text[0])
                item['exam_child_type'] = exam_text[0]
                item['list_href'] = prefix+exam_href[0]
                #print json.dumps(dict(item),indent=2, ensure_ascii=False)
                #print prefix+exam_href[0]
                yield scrapy.Request(url=prefix+exam_href[0], meta={'item':item}, callback=self.parse_index) 
                #print  item.items()
            if k == 0:
                #print json.dumps(dict(item),indent=2, ensure_ascii=False)
                #print prefix+exam_href[0]
                yield scrapy.Request(url=prefix+exam_href[0], meta={'item':item}, callback=self.parse_index) 
                #print  item.items()
            '''
            group_year_xpath = response.xpath('//*[@id="divLeftMenuTree"]/li[%d]/div' % index)     
            group_year_xpath_href = group_year_xpath.xpath('@href').extract()
            group_year_xpath_text = group_year_xpath.xpath('text()').extract()
            print group_year_xpath_text
            if group_year_xpath: 
                print group_year_xpath_text[0]
            '''
    def parse_index(self, response):
        #print "%"*100
        item = response.meta['item']
        #l = response.xpath('//*[@id="cont"]/div[5]/table/tbody/tr')
        l = response.xpath('//*[@id="cont"]/div[5]/table/tr')
        #print len(l)
        index = 0
        for tt in l:
            index = index + 1

            '''
            paper_rsp = response.xpath('//*[@id="cont"]/div[5]/table/tbody/tr[%d]/td[2]/a' % index)    
            paper_href = paper_rsp.xpath("@href").extract()
            paper_text = paper_rsp.xpath("text()").extract()
            paper_href_value = paper_href[0]
            paper_text_value = paper_text[0]
            '''

            paper_text = response.xpath('//*[@id="cont"]/div[5]/table/tr[%d]/td[2]/a/text()[1]' % index).extract()    
            paper_href = response.xpath('//*[@id="cont"]/div[5]/table/tr[%d]/td[2]/a/@href[1]' % index).extract()    
            update_time = response.xpath('//*[@id="cont"]/div[5]/table/tr[%d]/td[2]/span/text()[1]' % index).extract() 
            view_count = response.xpath('//*[@id="cont"]/div[5]/table//tr[%d]/td[2]/span/text()[2]' % index).extract() 
            download_count = response.xpath('//*[@id="cont"]/div[5]/table/tr[%d]/td[2]/span/text()[3]' % index).extract()
            '''
            print paper_text[0].strip()
            print paper_href[0].strip()
            print update_time[0].strip()
            print view_count[0].strip()
            print download_count[0].strip()
            '''


            item['paper_text'] = paper_text[0].strip()
            item['paper_href'] = paper_href[0].strip()
            item['update_time'] = update_time[0].strip()
            item['view_count'] = view_count[0].strip()
            item['download_count'] = download_count[0].strip()
            #print json.dumps(dict(item),indent=2, ensure_ascii=False)
            #print paper_href[0]
            yield scrapy.Request(url=paper_href[0], meta={'paper_href':paper_href}, callback=self.parse_paper) 
            exam_item_output(item)
            yield item
        #print "%"*100

    def parse_paper(self, response):

        item = PaperinationItem() 

        paper_href = response.meta['paper_href']
        paper_name = response.xpath('//*[@class="rpt-box"]/div[2]/div[1]/h1').extract()
        total_score = response.xpath('//*[@class="rpt-box"]/div[2]/div[1]/div[3]/text()[1]').extract()
        diff = response.xpath('//*[@class="rpt-box"]/div[2]/div[1]/div[3]/text()[2]').extract()
        view = response.xpath('//*[@class="rpt-box"]/div[2]/div[1]/div[3]/text()[3]').extract()
        download = response.xpath('//*[@class="rpt-box"]/div[2]/div[1]/div[3]/text()[4]').extract()
        
        item['paper_href'] = paper_href[0]        
        item['paper_name'] = paper_name[0]      
        item['total_score'] = total_score[0]       
        item['diffcult'] = diff[0]        
        item['view'] = view[0]        
        item['download'] = download[0]        

        index = 0 
        lstruct = {}
        part_list = response.xpath('//*[@class="rpt-box"]/div[2]/div[2]/h3').extract()
        for l in part_list: 
            part_list = []
            index = index + 1
            p = response.xpath('//*[@class="rpt-box"]/div[2]/div[2]/h3[%d]/text()' % (index )).extract()
            part_name = p[0]

            qindex = 0
            q_part = response.xpath('//*[@class="rpt-box"]/div[2]/div[2]/div[%d]/fieldset' % (index ))
            for q in q_part.extract():
                part_struct = {}
                qid = q_part.xpath('.//@id').extract()[qindex]
                qindex = qindex + 1 
                q_parse_href = response.xpath('//*[@class="rpt-box"]/div[2]/div[2]/div[%d]/span[%d]/a[1]/@href'%(index, qindex)).extract()[0]
                #print qid, q_parse_href
                part_struct['qid'] = qid
                part_struct['index'] = qindex 
                part_struct['href'] = q_parse_href 
                part_list.append(part_struct)

            lstruct[part_name] = part_list 
        item['lstruct'] = lstruct
        paper_item_output(item) 
        yield item



