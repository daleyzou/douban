# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class DoubanPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', port=3306, db='douban', user='root', passwd='root', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        print '--------------------------------------------'
        print item['title']
        print '--------------------------------------------'
        try:
            sql = "INSERT IGNORE INTO doubanmovies(title,bd,star,quote_mv,img_url) VALUES(\'%s\',\'%s\',%f,\'%s\',\'%s\')" %(item['title'], item['bd'], float(item['star']), item['quote'], item['title']+".jpg")
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print "----------------------inserted faild!!!!!!!!-------------------------------"
            print e.message
        return item

    def close_spider(self, spider):
        print '-----------------------quit-------------------------------------------'
        # 关闭数据库连接
        self.cur.close()
        self.conn.close()


# 下载图片
class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['img_url']
        # 添加meta是为了下面重命名文件名使用
        yield Request(image_url,meta={'title': item['title']})

    def file_path(self, request, response=None, info=None):
        title = request.meta['title']  # 通过上面的meta传递过来item
        image_guid = request.url.split('.')[-1]
        filename = u'{0}.{1}'.format(title, image_guid)
        print '++++++++++++++++++++++++++++++++++++++++++++++++'
        print filename
        print '++++++++++++++++++++++++++++++++++++++++++++++++'
        return filename


