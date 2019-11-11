import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class AnGang(BaseSpider):
    name = 'angang'
    allowed_domains = ['bid.ansteel.cn']
    start_urls = ['http://bid.ansteel.cn/ForePage/Skin4/NLList.aspx?page=1&pagesize=15&newstitle=&companyid=10697&xz=0']
    website_name = '鞍钢招标'
    tmpl_url = [ 'http://bid.ansteel.cn/ForePage/Skin4/NLList.aspx?page=%s&pagesize=15&newstitle=&companyid=10697&xz=0' % i for i in range(1, 10)]

    def __init__(self, *a, **kw):
        super(AnGang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//div[@class="cheenz"]//ul//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').get())
            item['title'] = a1.xpath(".//text()").get().strip()
            item['ctime'] = a1.xpath('..//..//span//text()').get()
            yield item


