from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import requests
import json


class AnHui(BaseSpider):
    name = 'anhui'
    allowed_domains = ['ggzy.ah.gov.cn']
    start_urls = ['http://ggzy.ah.gov.cn/bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1']
    website_name = '安徽公共资源交易'
    tmpl_url = 'http://ggzy.ah.gov.cn/dwr/call/plaincall/bulletinInfoDWR.getPackListForDwr1.dwr'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(AnHui, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 3


    def parse(self, response):
        headers = {'Host': 'ggzy.ah.gov.cn',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                   'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type': 'text/plain',
                   'Content-Length': '807',
                   # 'Cookie': 'insert_cookie = 98184645',
                   'Origin': 'http://ggzy.ah.gov.cn',
                   'Connection': 'keep-alive',
                   'Referer': 'http://ggzy.ah.gov.cn/bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1',
                   }
        for i in range(1, self.pageIndex):
            form_data = {
                'callCount': '1',
                'page': '/ bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1',
                'httpSessionId': 'a3d20a4a83460ca61ed779bebef1',
                'scriptSessionId': 'AD3F0852A1A1A78FA95118805EDE32E3222',
                'c0-scriptName': 'bulletinInfoDWR',
                'c0-methodName': 'getPackListForDwr1',
                'c0-id': '0',
                'c0-e1': 'string:2',
                'c0-e2': 'string:',
                'c0-e3': 'string:jy',
                'c0-e4': 'string:2',
                'c0-e5': 'string:',
                'c0-e6': 'string:',
                'c0-e7': 'string:',
                'c0-e8': 'number:2',
                'c0-e9': 'string:10',
                'c0-e10': 'string:true',
                'c0-e11': 'string:packTable',
                'c0-e12': 'string:44626',
                'c0-param0': 'Object_Object:{id:reference:c0-e1,hySort:reference:c0-e2,bulletinclass:reference:c0-e3,fileType:reference:c0-e4,bulletinType:reference:c0-e5,district:reference:c0-e6,srcdistrict:reference:c0-e7,currentPage:reference:c0-e8,pageSize:reference:c0-e9,isPage:reference:c0-e10,tabId:reference:c0-e11,totalRows:reference:c0-e12}',
                'batchId': '2'
            }

            r = requests.post(self.tmpl_url, data=form_data, headers=headers).text
            print(r)
            return

            # r = json.loads(r)
            #
            # for a1 in r['data']['records']:
            #     item = BiddinginfospiderItem()
            #     item['href'] = 'https://bidding.crmsc.com.cn/bulletin/look/' + str(a1['id'])
            #     item['title'] = a1['title']
            #     item['ctime'] = a1['awardPublishTime']
            #     yield item
