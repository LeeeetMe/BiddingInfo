import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class PuTian(BaseSpider):
    name = 'putian'
    allowed_domains = ['ggzyjy.xzfwzx.putian.gov.cn']
    start_urls = ['http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004003/004003002/?Paging=1']
    website_name = '莆田公共资源交易'
    tmpl_url = ['http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004003/004003002/?Paging=%s' % i for i in
                range(1, 10)] + ['http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/00400200500%s/' % i
                                 for i in range(2, 10)]

    def __init__(self, *a, **kw):
        super(PuTian, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//ul[@class="ewb-notice-items"]//li//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//@title").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//span//text()').extract_first()
            item['city'] = '莆田'
            yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//td[@id="TDContent"]//p')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        a=response.xpath('//table[@id="filedown"]')
        attach = a.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        print(item)
