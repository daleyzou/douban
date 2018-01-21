# -*- coding: utf-8 -*-
import scrapy

# noinspection PyUnresolvedReferences
from douban.items import DoubanItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['douban.com']
    offset = 0
    url = "https://movie.douban.com/top250?start="
    start_urls = [url + str(offset),]

    def parse(self, response):
        item = DoubanItem()
        movies = response.xpath("//div[ @class ='info']")
        links = response.xpath("//div[ @class ='pic']//img/@src").extract()
        for (each, link) in zip(movies,links):
            # 标题
            item['title'] = each.xpath('.//span[@class ="title"][1]/text()').extract()[0]
            # 信息
            item['bd'] = each.xpath('.//div[@ class ="bd"][1]/p/text()').extract()[0]
            # 评分
            item['star'] = each.xpath('.//div[@class ="star"]/span[@ class ="rating_num"]/text()').extract()[0]
            # 简介
            quote = each.xpath('.//p[@ class ="quote"] / span / text()').extract()
            # quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['quote'] = quote
            item['img_url'] = link

            yield item
        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url+str(self.offset), callback=self.parse)
