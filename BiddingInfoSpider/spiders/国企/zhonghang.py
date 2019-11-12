import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ZhongHang(BaseSpider):
    name = 'zhonghang'
    allowed_domains = ['bid.aited.cn']
    start_urls = ['http://bid.aited.cn/bid/index.html']
    website_name = '中航'
    tmpl_url = 'http://bid.aited.cn/front/ajax_getBidList.do'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(ZhongHang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 30

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'classId': '151',
                'key': '-1',
                'page': str(i),
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True )
            yield request
            # yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page,method='POST',body=json.dumps(form_data),)


    def parse_page(self, response):
        # a标签

        rs=eval(response.body.decode('utf8'))['list']
        selector=Selector(text=rs)
        a = selector.xpath('//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//@title").get().strip()
            item['ctime'] = a1.xpath('..//..//span//text()').get()
            yield item

