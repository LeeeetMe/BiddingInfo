import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import requests


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
            self.pageIndex = 10

    def start_requests(self):
        headers = {'Host': 'bidding.crmsc.com.cn',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                   'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Content-Type': 'application/json;charset=utf-8',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Content-Length': '102',
                   'Origin': 'https://bidding.crmsc.com.cn',
                   'Connection': 'keep-alive',
                   'Referer': 'https://bidding.crmsc.com.cn/bulletin',
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

            # r=requests.post(self.tmpl_url, data=json.dumps(form_data), headers=headers).text
            # r=json.loads(r)['data']['records']
            # print(r)
            # return

            yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page,method='POST',body=json.dumps(form_data),headers=headers,meta={"dynamic": True,})



    def parse_page(self, response):
        # a标签
        rs = response.body.decode('utf8')
        print(rs)
        return

        rs = json.loads(response.body.decode('utf8'))['data']['records']
        for a1 in rs:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//@title").get().strip()
            item['ctime'] = a1.xpath('..//..//span//text()').get()
            yield item
