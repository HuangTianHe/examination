# -*- coding: utf-8 -*-
import scrapy
import redis
import json
from examination.bingitems import BingItems , BingEgSenItems
from examination.util import * 


prefix = 'http://www.bing.com/dict/search?q='
r=redis.StrictRedis(host='172.18.4.81',port=6379,db=1)
class BingwordSpider(scrapy.Spider):
    name = "bingword"
    start_urls = (
        'http://www.baidu.com',
        'http://cn.bing.com/dict/search?intlF=0&q=right&FORM=HDRSC6'
    )

    def parse(self, response):
        item = BingItems()
        if response.url == "http://www.baidu.com":
            print 'continue'
        else:
            #en_word = response.meta['en_word']
            en_word = str(response.meta)
            pr_us  = response.xpath('//*[@class="hd_prUS"]/text()').extract()[0]
            gr = response.xpath('//*[@class="hd_pr"]/text()').extract()[0]
            audio_us = response.xpath('//*[@class="hd_tf"]/a/@onmouseover').extract()[0]
            audio = response.xpath('//*[@class="hd_tf"]/a/@onmouseover').extract()[1]
            item['en_word'] = en_word
            item['audio_us'] = audio_us
            item['audio_us_href'] = pr_us
            item['audio'] = audio
            item['audio_href'] = gr


            detail_list = response.xpath('//*[@class="qdef"]/ul/li')
            natures = []
            natures_meaning = []
            for d in detail_list:
                nature = d.xpath('.//span[@class="pos"]/text()').extract()
                meaning = d.xpath('.//span[@class="def"]/span/text()').extract()
                if not nature or not meaning:
                    continue
                natures.append(nature[0])
                natures_meaning.append(meaning[0])
              
            item['natures'] = natures
            item['natures_meaning'] = natures_meaning

            tense_name_list = response.xpath('.//div[@class="qdef"]/div[@class="hd_div1"]//div[@class="hd_if"]/span/text()').extract()
            tense_word_list= response.xpath('.//div[@class="qdef"]/div[@class="hd_div1"]//div[@class="hd_if"]/a/text()').extract()
            tense_href_list = response.xpath('.//div[@class="qdef"]/div[@class="hd_div1"]//div[@class="hd_if"]/a/@href').extract()
            item['tense_names'] = tense_name_list
            item['tense_words'] = tense_word_list

            #detail_list = response.xpath('//div[@class="qdef"]/div[@class="wd_div"]/div[@id="thesaurusesid"]/div[@id="synoid"]/div[@class="df_div2"]/div[@class="de_title1"]/text()')
            #response.xpath('//div[@id="synoid"]//div[@class="col_fl"]/a/span/text()')

            #tongyi
            synoid_natures = response.xpath('//div[@id="synoid"]//div[@class="de_title1"]/text()').extract()
            synoid_list = response.xpath('//div[@id="synoid"]//div[@class="df_div2"]')
            synoid_words_list = []
            for d in synoid_list:
                synoid_words = d.xpath('.//div[@class="col_fl"]/a/span/text()').extract()
                synoid_words_list.append(synoid_words)

            item['synonymous_nature'] = synoid_natures
            item['synonymous_words'] = synoid_words_list

            #DAPEI
            colid_natures = response.xpath('//div[@id="colid"]//div[@class="de_title2"]/text()').extract()
            colid_list = response.xpath('//div[@id="colid"]//div[@class="df_div2"]')
            colid_words_list = []
            for d in colid_list:
                colid_words = d.xpath('.//div[@class="col_fl"]/a/span/text()').extract()
                colid_words_list.append(colid_words)

            item['phrase_nature'] = colid_natures
            item['phrase_words'] = colid_words_list

            #FANYI
            antoid_natures = response.xpath('//div[@id="synoid"]//div[@class="de_title1"]/text()').extract()
            antoid_list = response.xpath('//div[@id="antoid"]//div[@class="df_div2"]')
            antoid_words_list = []
            for d in antoid_list:
                antoid_words = d.xpath('.//div[@class="col_fl"]/a/span/text()').extract()
                antoid_words_list.append(antoid_words)
            item['antonym_nature'] = antoid_natures
            item['antonym_words'] =  antoid_words_list


            #EN-EN
            #response.xpath('.//div[@id="homoid"]/table//tr[@class="def_row df_div1"][1]/td/div[@class="def_fl"]/div[@class="de_li1 de_li3"]/div/text()').extract()
            homoid_list = response.xpath('.//div[@id="homoid"]/table//tr[@class="def_row df_div1"]/td/div[@class="pos pos1"]/text()').extract()
            detail_en_list = response.xpath('.//div[@id="homoid"]/table//tr[@class="def_row df_div1"]')
            for detail_en in detail_en_list:
                detail_en_list = detail_en.xpath('.//td/div[@class="def_fl"]/div[@class="de_li1 de_li3"]/div/text()').extract()
            item['en2en_explain_nature'] = homoid_list
            item['en2en_explain_sentence'] =  detail_en_list
                

           
            #response.xpath('//*[@id="sentenceSeg"]/div[1]/div[2]/div[1]/a[3]')
      

            explain_list = response.xpath('//*[@class="senDefLink"]/a/text()').extract()
            item['cn_meaning'] =  explain_list
            print "*"*100 
            bing_item_output(item)
            print "*"*100 
            yield item
            for t in explain_list:
                if t == 'All':
                    continue
                surl = 'http://www.bing.com/dict/service?q='+en_word+'%20'+t+'&dtype=sen'
                print surl
                yield scrapy.Request(url=surl,meta={'en_word':en_word, 'word':t},callback=self.parse_sentence) 


        word_tuple = r.brpop('words', 10)
        if word_tuple:
            en_word =  word_tuple[1]
            yield scrapy.Request(url=prefix+en_word,meta={'en_word':en_word},callback=self.parse) 
        else:
            print 'spider over'
            return
    def parse_sentence(self, response):
        
        word = response.meta['word']
        en_word = response.meta['en_word']
        item = BingEgSenItems()
        sentence_list = response.xpath('//*[@class="se_li"]')
        eg_sentence ={}
        eg_sentence['word'] = word
        cn_list= [] 
        en_list= [] 
        for s in sentence_list: 
            en = s.xpath('.//*[@class="se_li1"]//*[@class="sen_en"]//text()').extract()
            cn= s.xpath('.//*[@class="se_li1"]//*[@class="sen_cn"]//text()').extract()
            cn_list.append(cn)
            en_list.append(en)
        eg_sentence['cn_list'] = cn_list
        eg_sentence['en_list'] = en_list
        item['eg_sentence'] = eg_sentence
        item['en_word'] = en_word
        #print json.dumps(item, indent=2, ensure_ascii=True)
        #print item
        print "="*100 
        bing_sen_output(item)
        print "="*100 
        yield  item      
