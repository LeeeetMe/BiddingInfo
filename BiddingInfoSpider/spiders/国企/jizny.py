import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class JiZhongNY(BaseSpider):
    name = 'jzny'
    allowed_domains = ['www.jzbidding.com']
    start_urls = ['http://www.jzbidding.com/jznycms/category/belletinList.html?searchDate=1994-11-11&dates=300&word=&categoryId=88&industryName=&status=&page=1']
    website_name = '冀中电力招投标'
    tmpl_url = [ 'http://www.jzbidding.com/jznycms/category/belletinList.html?searchDate=1994-11-11&dates=300&word=&categoryId=88&industryName=&status=&page=%s' % i for i in range(1, 20)]

    def __init__(self, *a, **kw):
        super(JiZhongNY, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//ul[@class="newslist"]//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//h1//text()").getall()[3].strip()
            item['ctime'] = a1.xpath('normalize-space(string(.//div[@class="newsDate"]))').get().replace('/','-').replace(' ','-')
            yield item


