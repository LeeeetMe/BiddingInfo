import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ZhaoShangJu(BaseSpider):
    name = 'zhaoshangju'
    allowed_domains = ['dzzb.ciesco.com.cn']
    start_urls = ['https://dzzb.ciesco.com.cn/gg/ggList']
    website_name = '招商局招标'
    tmpl_url = 'https://dzzb.ciesco.com.cn/gg/ggList'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(ZhaoShangJu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 10

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'currentpage': str(i),
                'xmLeiXing': '',
                'xm_BH': '',
                'ggName': '',
                'zbr': '',
                'danWeiName': ''

            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True,meta={"dynamic": True,})
            yield request
            # yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page,method='POST',body=json.dumps(form_data),)

    def parse_page(self, response):
        # a标签
        rs = response.body.decode('utf8')
        # selector=Selector(text=rs)

        a = response.xpath('//div[@class="zbgg_table"]//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//@title").get().strip()
            item['ctime'] = a1.xpath('..//..//..//td[5]//text()').get().strip()
            yield item
