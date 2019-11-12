import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ZhongMei(BaseSpider):
    name = 'zhongmei'
    allowed_domains = ['www.zmzb.com']
    start_urls = ['http://www.zmzb.com/zbgg/index_1.jhtml']
    website_name = '中煤'
    tmpl_url = [ 'http://www.zmzb.com/zbgg/index_%s.jhtml' % i for i in range(1, 20)]

    def __init__(self, *a, **kw):
        super(ZhongMei, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//div[@class="lb-link"]//ul//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//@title").get().strip()
            item['ctime'] = a1.xpath('.//span[@class="bidDate"]//text()').get()
            yield item


