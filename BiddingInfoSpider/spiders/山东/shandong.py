import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ShanDong(BaseSpider):
    name = 'shandong'
    allowed_domains = ['ggzyjyzx.shandong.gov.cn']
    start_urls = ['http://ggzyjyzx.shandong.gov.cn/003/moreinfo.html']
    website_name = '山东公共资源交易'
    tmpl_url = ['http://ggzyjyzx.shandong.gov.cn/003/moreinfo.html'] + [
        'http://ggzyjyzx.shandong.gov.cn/003/%s.html' % i for i in range(2, 30)]

    def __init__(self, *a, **kw):
        super(ShanDong, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//ul[@class="ewb-list"]//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//@title").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//span[@class="ewb-list-date"]//text()').extract_first()
            item['city'] = '山东'
            yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@id="infocont"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        print(item)
