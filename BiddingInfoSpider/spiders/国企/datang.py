import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import json
import time, datetime


class DaTang(BaseSpider):
    name = 'datang'
    allowed_domains = ['www.cdt-ec.com']
    start_urls = [
        'http://www.cdt-ec.com/potal-web/pendingGxnotice/where?publish_time=&publish_times=&purchase_unit=&message_title=&message_type=0&pageno=1&pagesize=150']
    website_name = '大唐集团'
    tmpl_url = [
        'http://www.cdt-ec.com/potal-web/pendingGxnotice/where?publish_time=&publish_times=&purchase_unit=&message_title=&message_type=0&pageno=1&pagesize=150']

    def __init__(self, *a, **kw):
        super(DaTang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        rs = json.loads(response.body.decode('utf8'))

        for a1 in rs:
            item = BiddinginfospiderItem()
            item['href'] = a1['pdf_url']
            item['title'] = a1['message_title']
            time0 = time.localtime(int(str(a1['publish_time'])[0:10]))
            item['ctime'] = time.strftime("%Y-%m-%d", time0)
            yield item
