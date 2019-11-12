# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json


class BiddinginfospiderPipeline(object):
    def process_item(self, item, spider):
        item['web_site'] = spider.website_name
        # if item.get('content'):
        #     print('content len is', len(item['content']))
        #     item['content'] = 'newline'.join(item['content'])
        # else:
        #     item['content'] = ""
        # x = json.dumps(item)
        # print(x)
        return item
