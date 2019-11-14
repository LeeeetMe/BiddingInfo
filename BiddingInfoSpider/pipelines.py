# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import redis
from scrapy.exceptions import DropItem


class BiddinginfospiderPipeline(object):
    def __init__(self, host, port, set_name):
        self.set_name = set_name
        self.pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)

        print("数据", self.r.scard(self.set_name))

    def process_item(self, item, spider):
        item['web_site'] = spider.website_name
        href_md5 = self.md5(item.get("href"))
        print('href for md5 is', href_md5)
        if href_md5:
            if self.r.sismember(self.set_name, href_md5):
                print("数据已经存在", item)
                # 如果该条数据存在则删除该item
                # raise DropItem("Duplicate item found: %s" % item['web_site'])
                # 如果全部数据都存在，导出item设置为默认为空的值，防止一条数据都没有的情况下xsl文件无法打开
                return {"web_site": "",
                        "city": "", "category": "",
                        "industry": "",
                        "code": "", "title": "",
                        "ctime": "", "href": ""}
            else:
                self.r.sadd(self.set_name, href_md5)
                return item

    def close_spider(self, spider):
        self.r.close()

    def md5(self, url):
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        return obj.hexdigest()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            set_name=crawler.settings.get('REDIS_SET'),
        )
