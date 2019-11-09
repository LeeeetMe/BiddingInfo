"""http://www.hnsggzy.com/queryContent_1-jygk.jspx?title=&origin=&inDates=30&channelId=846&ext=%E6%8B%9B%E6%A0%87/%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime="""
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class HuNan(BaseSpider):
    name = 'HuNan'
    allowed_domains = ['hnsggzy.com']
    start_urls = [
        'http://www.hnsggzy.com/queryContent_1-jygk.jspx?title=&origin=&inDates=30&channelId=846&ext=%E6%8B%9B%E6%A0%87/%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime=']
    website_name = '湖南省公共资源交易服务平台'
    tmpl_url = "http://www.hnsggzy.com/queryContent_{0}-jygk.jspx?title=&origin=&inDates=30&channelId=846&ext=%E6%8B%9B%E6%A0%87/%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime="
    category = ""

    def __init__(self, *a, **kw):
        super(HuNan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 20)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//ul[@class="article-list2"]//li')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')
            title = a.xpath('normalize-space(string(.))').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(l.xpath('.//div[@class="list-times"]//text()'))
            other_data = l.xpath('.//div[@class="list-t2"]').xpath('normalize-space(string(.))').extract()
            city = other_data[0].split("：")[1]
            category = other_data[2].split("：")[1]
            item.update(
                city=city,
                category=category,
                title=title,
                ctime=ctime,
                href=href,
            )
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})
            yield item

    def parse_item(self, response):
        item = response.meta["item"]

        print(response.url)
        article = response.xpath('//div[@class="content-article"]//p')
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
