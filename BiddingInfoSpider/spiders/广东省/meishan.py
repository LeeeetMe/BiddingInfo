import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class MeiShan(BaseSpider):
    name = 'meishan'
    allowed_domains = ['www.msggzy.org.cn']
    start_urls = ['http://www.msggzy.org.cn/front/jsgc/001002/?Paging=1']
    website_name = '眉山公共资源交易'
    tmpl_url = ['http://www.msggzy.org.cn/front/jsgc/001002/?Paging=%s' % i for i in range(1, 5)]

    def __init__(self, *a, **kw):
        super(MeiShan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//div[@class="ewb-comp-bd"]//table//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//@title").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//td[2]//text()').extract_first()
            item['city'] = '眉山'

            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//td[@id="mainContent"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        # print(item)
        yield item
