
import scrapy

class BingItems(scrapy.Item):
    en_word = scrapy.Field()
    audio_us = scrapy.Field()
    audio_us_href = scrapy.Field()
    audio = scrapy.Field()
    audio_href = scrapy.Field()
    natures = scrapy.Field()
    natures_meaning = scrapy.Field()
    tense_names = scrapy.Field()
    tense_words = scrapy.Field()
    phrase_nature = scrapy.Field()
    phrase_words = scrapy.Field() 
    synonymous_nature = scrapy.Field() 
    synonymous_words = scrapy.Field() 
    antonym_nature = scrapy.Field()
    antonym_words = scrapy.Field()
    en2en_explain_nature = scrapy.Field()
    en2en_explain_sentence = scrapy.Field()
    cn_meaning  = scrapy.Field()


class BingEgSenItems(scrapy.Item):
    en_word = scrapy.Field()
    eg_sentence = scrapy.Field()

