import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class GuangZhou(BaseSpider):
    name = 'guangzhou'
    allowed_domains = ['www.gzebpubservice.cn']
    start_urls = ['http://www.gzebpubservice.cn/fjzbgg/index.htm']
    website_name = '广州公共资源交易'
    tmpl_url = ['http://www.gzebpubservice.cn/fjzbgg/index_%s.htm' % i for i in range(2, 30)] + [
        'http://www.gzebpubservice.cn/jtzbgg/index_%s.htm' % i for i in range(1, 30)] + [
                   'http://www.gzebpubservice.cn/dlzbgg/index_%s.htm' % i for i in range(1, 20)] + [
                   'http://www.gzebpubservice.cn/tlzbgg/index_%s.htm' % i for i in range(1, 10)]

    def __init__(self, *a, **kw):
        super(GuangZhou, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//div[@class="prcont TableListLine"]//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//@title").extract_first().strip()
            item['ctime'] = a1.xpath('.//span//text()').extract_first()
            item['city'] = '广州'
            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@class="Section1"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            '..//a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        print(item)
