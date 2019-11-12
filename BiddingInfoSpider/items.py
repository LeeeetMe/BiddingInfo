# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiddinginfospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    web_site = scrapy.Field()
    code = scrapy.Field()
    title = scrapy.Field()
    ctime = scrapy.Field()
    href = scrapy.Field()
    # 种类
    category = scrapy.Field()
    city = scrapy.Field()
    # 行业
    industry = scrapy.Field()
