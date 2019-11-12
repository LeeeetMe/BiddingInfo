import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class HeNan(BaseSpider):
    name = 'henan'
    allowed_domains = ['hnsggzyfwpt.hndrc.gov.cn']
    start_urls = ['http://hnsggzyfwpt.hndrc.gov.cn/002/tradePublic.html']
    website_name = '河南公共资源交易'
    tmpl_url = [
        'http://hnsggzyfwpt.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex=%s&pageSize=22&day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002001001&siteguid=9f5b36de-4e8f-4fd6-b3a1-a8e08b38ea38' % i
        for i in range(1, 100)]


    def __init__(self, *a, **kw):
        super(HeNan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        rs = json.loads(response.body.decode('utf8'))
        rs=eval(rs['return'])['Table']
        for a in rs:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a['href'])
            item['title'] = a['title']
            item['ctime'] = a['infodate']
            item['city'] =a['infoc']

            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item


    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@class="ewb-left-bd"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments
        # print(item)
        yield item
