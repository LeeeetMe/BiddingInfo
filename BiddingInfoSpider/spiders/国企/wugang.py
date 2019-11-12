import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class WuGang(BaseSpider):
    name = 'wugang'
    allowed_domains = ['wiscobidding.com.cn']
    start_urls = ['http://www.wiscobidding.com.cn/zbgg/index_1.jhtml']
    website_name = '武钢电子招投标'
    tmpl_url = [ 'http://www.wiscobidding.com.cn/zbgg/index_%s.jhtml' % i for i in range(1, 10)]

    def __init__(self, *a, **kw):
        super(WuGang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//div[@class="lb-link"]//ul//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//@title").get().strip()
            item['ctime'] = a1.xpath('.//span[3]//text()').get()
            yield item


