import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class HaiNan(BaseSpider):
    name = 'hainan'
    allowed_domains = ['zw.hainan.gov.cn']
    start_urls = ['http://zw.hainan.gov.cn/ggzy/ggzy/jgzbgg/index_1.jhtml']
    website_name = '海南省公共资源'
    tmpl_url = ['http://zw.hainan.gov.cn/ggzy/ggzy/jgzbgg/index_%s.jhtml' % i for i in range(1, 50)]

    def __init__(self, *a, **kw):
        super(HaiNan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//table[@class="newtable"]//a')

        for a1 in a[0:9]:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//text()").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//td[4]//text()').extract_first()
            item['city'] = a1.xpath('..//..//td[2]//text()').extract_first()

            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item


    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@class="newsCon"]//div')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        print(item)
