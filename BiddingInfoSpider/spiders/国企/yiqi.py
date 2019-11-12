import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class YiQi(BaseSpider):
    name = 'yiqi'
    allowed_domains = ['etp.fawiec.com']
    start_urls = ['https://etp.fawiec.com/gg/ggList?zbLeiXing=1&xmLeiXing=&ggStartTimeEnd=']
    website_name = '中国一汽'
    tmpl_url = 'https://etp.fawiec.com/gg/ggList?zbLeiXing=1&xmLeiXing=&ggStartTimeEnd='
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(YiQi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 30

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'currentPage': str(i),
                'ggName': '',
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True )
            yield request

    def parse_page(self, response):
        # a标签
        a = response.xpath('//div[@class="detail clearfloat"]//ul//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//text()").get().strip()
            item['ctime'] = a1.xpath('..//..//..//span[@class="fr"]//text()').get()
            yield item

