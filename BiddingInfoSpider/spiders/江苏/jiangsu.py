from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest


class JiangSu(BaseSpider):
    name = 'JiangSu'
    allowed_domains = ['bulletin.jszbtb.com']
    start_urls = [
        'http://bulletin.jszbtb.com/xxfbcms/index.html?0&categoryId=88&status=01&startcheckDate=2019-10-01&endcheckDate=2019-11-05&page=1']
    website_name = '江苏省招标投标公共服务平台'
    tmpl_url = 'http://bulletin.jszbtb.com/xxfbcms/index.html?0&categoryId=88&status=01&startcheckDate=2019-10-01&endcheckDate=2019-11-05&page={0}'

    def __init__(self, *a, **kw):
        super(JiangSu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 150)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//table[@class="table_text"]//tr')
        for l in li[1:]:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')
            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(a.xpath('.//td[5]//span//text()'))
            industry = l.xpath(".//td[2]//span//text()").extract_first()
            city = l.xpath(".//td[3]//span//@title").extract_first()
            item.update(
                industry=industry,
                title=title,
                ctime=ctime,
                href=href,
                city=city,
            )
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})
            yield item

    def parse_item(self, response):
        item = response.meta.get("item")
        print(response.url)
        article = response.xpath('//div[@class="mian_list"]')

        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        swf = response.xpath('//div[@class="mian_list_03"]//script//text()').extract_first()
        swf = self.get_swf(swf)
        attachments = article.xpath(
            './/a[contains(@href,".pdf") \
            or contains(@href,".rar") \
            or contains(@href,".doc") \
            or contains(@href,".xls") \
            or contains(@href,".zip") \
            or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)
        attachments_dict.update({"swf": swf})
        item.update(
            content=content,
            attachments=attachments_dict
        )
        print(item)
        # yield item

    def get_swf(self, s):
        s = "".join(s.split())
        start = s.index("escape('")
        end = s.index("'),EncodeURI")
        result = s[start + 8:end]
        return result
