import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import json


class TieJianSB(BaseSpider):
    name = 'tiejiansb'
    allowed_domains = ['ece.crcc.cn']
    start_urls = [
        'http://ece.crcc.cn/homepage/queryInviteList.jhtml?page=1&invitename=&invitecode=&beginTime=&endTime=&start=0&limit=20']
    website_name = '铁建设备'
    tmpl_url = [
        'http://ece.crcc.cn/homepage/queryInviteList.jhtml?page=1&invitename=&invitecode=&beginTime=&endTime=&start=%s&limit=20' % i
        for i in range(0, 100, 20)]

    def __init__(self, *a, **kw):
        super(TieJianSB, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        rs = json.loads(response.body.decode('utf8'))
        rs = rs['_rows']
        for a1 in rs:
            item = BiddinginfospiderItem()
            item['href'] = 'http://ece.crcc.cn/homepage/inviteInfo.jhtml?type=1&id=' + str(a1['inviteid'])
            item['title'] = a1['texttitle']
            item['ctime'] = a1['recordtime'][0:10]
            yield item


class TieJianWZ(BaseSpider):
    name = 'tiejianwz'
    allowed_domains = ['ece.crcc.cn']
    start_urls = ['http://ecm.crcc.cn/unlogin/queryPurchase.jhtml?model=1&start=0&limit=20']
    website_name = '铁建物资'
    tmpl_url = [
        'http://ecm.crcc.cn/unlogin/queryPurchase.jhtml?model=1&title=&code=&pubstartdate=&pubenddate=&orgname=&start=%s&limit=20' % i
        for i in range(0, 100, 20)]
    'http://ecm.crcc.cn/unlogin/queryPurchase.jhtml?model=1&start=%s&limit=20'

    def __init__(self, *a, **kw):
        super(TieJianWZ, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        rs = json.loads(response.body.decode('utf8'))
        rs = rs['_rows']
        for a1 in rs:
            item = BiddinginfospiderItem()
            item['href'] = 'http://ecm.crcc.cn/unlogin/queryPurchaseTenderDetailInit.jhtml?model=1&id=' + a1['id']
            item['title'] = a1['v_notice_title']
            item['ctime'] = a1['d_createdate']
            yield item
