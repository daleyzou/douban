# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    bd = scrapy.Field()
    star = scrapy.Field()
    quote = scrapy.Field()
    img_url = scrapy.Field()
    pic_path = scrapy.Field()

