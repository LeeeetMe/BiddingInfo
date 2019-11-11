import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class NanWang(BaseSpider):
    name = 'nanwang'
    allowed_domains = ['ggzy.np.gov.cn']
    start_urls = ['http://www.bidding.csg.cn/zbgg/index_1.jhtml']
    website_name = '南网电子商务'
    tmpl_url = ['http://www.bidding.csg.cn/zbgg/index_%s.jhtml' % i for i in range(1, 50)]

    def __init__(self, *a, **kw):
        super(NanWang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        a = response.xpath('//div[@class="W750 Right"]//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            href = response.urljoin(a1.xpath('.//@href').extract_first())
            title = a1.xpath(".//text()").extract_first().strip()
            ctime = a1.xpath('..//..//span//text()').extract_first()
            city = '南方电网'
            item.update(
                href=href,
                title=title,
                ctime=ctime,
                city=city
            )
            yield item
            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
