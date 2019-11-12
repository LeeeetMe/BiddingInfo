from datetime import date

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class ShenHua(BaseSpider):
    name = 'ShenHua'
    allowed_domains = ['shenhuabidding.com.cn']
    start_urls = ['http://www.shenhuabidding.com.cn/bidweb/001/001002/001002001/1.html']
    website_name = '神华招标网'
    tmpl_url = 'http://www.shenhuabidding.com.cn/bidweb/001/001002/001002001/{0}.html'
    category = ""
    industry = "货物"

    def __init__(self, *a, **kw):
        super(ShenHua, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 50)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//li[@class="right-item clearfix"]')
        for l in li:
            a = l.xpath('.//a[@class="infolink"]')
            item = BiddinginfospiderItem()
            title = a.xpath(".//@title").get()
            href = response.urljoin(a.xpath('.//@href').get())
            code = l.xpath('.//span[@class="author"]//text()').get()
            ctime = self.get_ctime(l.xpath('.//span[@class="r"]//text()'))

            item.update(
                code=code,
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            print(item)
            # yield item


class ShenHuaGongCheng(BaseSpider):
    name = 'ShenHuaGongCheng'
    allowed_domains = ['shenhuabidding.com.cn']
    start_urls = ['http://www.shenhuabidding.com.cn/bidweb/001/001002/001002002/1.html']
    website_name = '神华招标网'
    tmpl_url = 'http://www.shenhuabidding.com.cn/bidweb/001/001002/001002002/{0}.html'
    category = ""
    industry = "工程"

    def __init__(self, *a, **kw):
        super(ShenHuaGongCheng, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 10)])


class ShenHuaFuWu(BaseSpider):
    name = 'ShenHuaFuWu'
    allowed_domains = ['shenhuabidding.com.cn']
    start_urls = ['http://www.shenhuabidding.com.cn/bidweb/001/001002/001002003/1.html']
    website_name = '神华招标网'
    tmpl_url = 'http://www.shenhuabidding.com.cn/bidweb/001/001002/001002003/{0}.html'
    category = ""
    industry = "服务"

    def __init__(self, *a, **kw):
        super(ShenHuaFuWu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 21)])
