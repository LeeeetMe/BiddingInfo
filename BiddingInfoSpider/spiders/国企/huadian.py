import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class HuaDian(BaseSpider):
    name = 'huadian'
    allowed_domains = ['www.chdtp.com']
    start_urls = ['https://www.chdtp.com/pages/wzglS/zbgg/zhaobiaoList.jsp']
    website_name = '华电招投标'
    tmpl_url = 'https://www.chdtp.com/webs/queryWebZbgg.action'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(HuaDian, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 10

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'zbggType': '1',
                'page.pageSize': '31',
                'page.currentpage': str(i),
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True )
            yield request
            # yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page,method='POST',body=json.dumps(form_data),)


    def parse_page(self, response):
        # a标签

        rs=response.body.decode('utf8')
        selector=Selector(text=rs)
        a = selector.xpath('//table[@class="wwFormTable"]//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = 'https://www.chdtp.com/staticPage/'+a1.xpath('.//@href').get()[25:-2]
            item['title'] = a1.xpath(".//@title").get().strip()
            item['ctime'] = a1.xpath('..//..//..//td[2]//span[@class="index_s12_c666"]//text()').get()[1:-1]
            yield item

