
import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class TianJin(BaseSpider):
    name = 'TianJin'
    allowed_domains = ['tsjj.com.cn']
    start_urls = ['http://www.tsjj.com.cn/zbgg.asp?upid=0&typeid=105&t=4&page=1']
    website_name = '天津水务有形市场'
    tmpl_url = 'http://www.tsjj.com.cn/zbgg.asp?upid=0&typeid=105&t=4&page={0}'
    # category = ""


    def __init__(self, *a, **kw):
        super(TianJin, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 5)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//div[@class="jianjie"]//tr')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')
            title = a.xpath('.//text()').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            # ctime = self.get_ctime(a.xpath('.//span//text()'))
            item.update(
                # category=self.category,
                title=title,
                # ctime=ctime,
                href=href,
            )
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})
            yield item

    def parse_item(self, response):
        item = response.meta["item"]

        print(response.url)
        article = response.xpath('//div[@class="jianjie"]//p')
        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attachments = article.xpath(
            './/a[contains(@href,".pdf") \
            or contains(@href,".rar") \
            or contains(@href,".doc") \
            or contains(@href,".xls") \
            or contains(@href,".zip") \
            or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)
        item.update(
            content=content,
            attachments=attachments_dict
        )
        # print(item)
        yield item
