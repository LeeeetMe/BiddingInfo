from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import requests
import json


class ZhongTieWu(BaseSpider):
    name = 'zhongtiewu'
    allowed_domains = ['bidding.crmsc.com.cn']
    start_urls = ['https://bidding.crmsc.com.cn/bulletin/']
    website_name = '中铁物'
    tmpl_url = 'https://bidding.crmsc.com.cn/bulletin/list'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(ZhongTieWu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 3

    def parse(self, response):
        headers = {'Host': 'bidding.crmsc.com.cn',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                   'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Content-Type': 'application/json;charset=utf-8',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Content-Length': '102',
                   # 'Cookie': 'insert_cookie = 98184645',
                   'Origin': 'https://bidding.crmsc.com.cn',
                   'Connection': 'keep-alive',
                   'Referer': 'https://bidding.crmsc.com.cn/bulletin/',
                   }
        for i in range(1, self.pageIndex):
            form_data = {
                'pageSize': 15,
                'key': '',
                'currentPage': str(i),
                'bidType': '',
                'bulletinType': '',
                'purchaseMode': '',
                'time': '0',
            }

            r=requests.post(self.tmpl_url, data=json.dumps(form_data), headers=headers).text
            r=json.loads(r)

            for a1 in r['data']['records']:
                item = BiddinginfospiderItem()
                item['href'] = 'https://bidding.crmsc.com.cn/bulletin/look/'+str(a1['id'])
                item['title'] = a1['title']
                item['ctime'] = a1['awardPublishTime']
                yield item



    #另一种思路 初步结果通过meta传送到page
    # def start_requests(self):
    #     headers = {'Host': 'bidding.crmsc.com.cn',
    #                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    #                'Accept': '*/*',
    #                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #                'Accept-Encoding': 'gzip, deflate, br',
    #                'Content-Type': 'application/json;charset=utf-8',
    #                'X-Requested-With': 'XMLHttpRequest',
    #                'Content-Length': '102',
    #                'Cookie': 'insert_cookie = 98184645',
    #                'Origin': 'https://bidding.crmsc.com.cn',
    #                'Connection': 'keep-alive',
    #                'Referer': 'https://bidding.crmsc.com.cn/bulletin/',
    #                }
    #     for i in range(1, self.pageIndex):
    #         form_data = {
    #             'pageSize': 15,
    #             'key': '',
    #             'currentPage': str(i),
    #             'bidType': '',
    #             'bulletinType': '',
    #             'purchaseMode': '',
    #             'time': '0',
    #         }
    #
    #         r = requests.post(self.tmpl_url, data=json.dumps(form_data), headers=headers).text
    #         r = json.loads(r)
    #         yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page, meta={'meta': r, })
    #
    # def parse_page(self, response):
    #     r = response.meta['meta']['data']['records']
    #     for a1 in r:
    #         item = BiddinginfospiderItem()
    #         item['href'] = 'https://bidding.crmsc.com.cn/bulletin/look/'+str(a1['id'])
    #         item['title'] = a1['title']
    #         item['ctime'] = a1['awardPublishTime']
    #         yield item