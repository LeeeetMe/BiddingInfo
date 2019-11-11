import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import json


class LangChao(BaseSpider):
    name = 'langchao'
    allowed_domains = ['scs.inspur.com']
    start_urls = [
        'http://scs.inspur.com/MetaPortlet/EPP/GGList/ConfigTools/CEPPWebHandler.ashx?projectType=all&ggtype=CRFQ&relTime=0&keyWord=&pageSort=desc&tagFlag=0&pageIndex=1&rowCount=100&isOpenOnly=True&canOpenDetal=True']
    website_name = '浪潮集团电子采购'
    tmpl_url = [
        'http://scs.inspur.com/MetaPortlet/EPP/GGList/ConfigTools/CEPPWebHandler.ashx?projectType=all&ggtype=CRFQ&relTime=0&keyWord=&pageSort=desc&tagFlag=0&pageIndex=1&rowCount=100&isOpenOnly=True&canOpenDetal=True']

    def __init__(self, *a, **kw):
        super(LangChao, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        rs=json.loads(response.body.decode('utf8'))
        rs=rs['RESULT']


        for a1 in rs:
            item = BiddinginfospiderItem()
            item['href'] = 'http://scs.inspur.com/GGDetail.htm?dataType=CRFQ&id='+a1['NoticeID']
            item['title'] = a1['NoticeTitle']
            item['ctime'] = a1['PubTime'][0:10]
            yield item
