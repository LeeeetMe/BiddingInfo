from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from scrapy import FormRequest


class ZhongHaiYou(BaseSpider):
    name = 'ZhongHaiYou'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = ['https://buy.cnooc.com.cn/cbjyweb/001/001001/1.html']
    website_name = '中国海洋石油集团有限公司采办业务管理与交易系统'
    tmpl_url = 'https://buy.cnooc.com.cn/cbjyweb/001/001001/{0}.html'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super(ZhongHaiYou, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, self.endPageNum)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//li[@class="now-hd-items clearfix"]')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('./a')
            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(l.xpath('.//span//text()'))
            item.update(
                title=title,
                ctime=ctime,
                href=href,
            )
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})
            yield item


    def parse_item(self, response):
        item = response.meta.get("item")
        print(response.url)
        article = response.xpath('//div[@class="article-main"]//p|//div[@class="article-main"]//div')
        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attachments = response.xpath(
            './/a[contains(@href,".pdf") \
            or contains(@href,".rar") \
            or contains(@href,".doc") \
            or contains(@href,".xls") \
            or contains(@href,".zip") \
            or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)
        item.update(
            content=content,
            attachments=attachments_dict,
        )
        # print(item)
        yield item
