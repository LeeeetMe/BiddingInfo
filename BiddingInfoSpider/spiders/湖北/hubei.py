"""http://www.hnsggzy.com/queryContent_1-jygk.jspx?title=&origin=&inDates=30&channelId=846&ext=%E6%8B%9B%E6%A0%87/%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime="""
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class HuBei(BaseSpider):
    name = 'HuBei'
    allowed_domains = ['hbggzy.cn']
    start_urls = ['http://www.hbggzy.cn/jydt/003001/003001002/1.html']
    website_name = '湖北省公共资源交易网'
    tmpl_url = 'http://www.hbggzy.cn/jydt/003001/003001002/{0}.html'
    category = ""

    def __init__(self, *a, **kw):
        super(HuBei, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 11)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//ul[@class="ewb-news-items"]//li')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')
            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(a.xpath('.//span//text()'))

            item.update(
                city="湖北",
                title=title,
                ctime=ctime,
                href=href,
            )
            yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta["item"]

        print(response.url)
        article = response.xpath('//div[@class="news-article-para"]//tr')
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
        print(item)
        # yield item
