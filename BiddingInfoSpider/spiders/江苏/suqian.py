import json
import scrapy
from scrapy import FormRequest
from urllib.parse import urljoin
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class SuQian(BaseSpider):
    name = 'suqian'
    allowed_domains = ['ggzy.sqzwfw.gov.cn']
    start_urls = ['http://ggzy.sqzwfw.gov.cn/jyxx/tradeInfo.html']
    website_name = '宿迁公共资源交易'
    tmpl_url = 'http://ggzy.sqzwfw.gov.cn/WebBuilder/jyxxAction.action?cmd=getList'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(SuQian, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 100

    def start_requests(self):
        for i in range(self.pageIndex):
            form_data = {
                'categorynum': '001',
                'pageIndex': str(i),
                'pageSize': '15',
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True)
            yield request

    def parse_page(self, response):
        rs = json.loads(response.body.decode('utf8'))
        for l in json.loads(rs['custom'])['Table']:
            title = l['title']
            href = response.urljoin(l['href'])
            ctime = l['postdate']
            city = l['city']
            item = BiddinginfospiderItem(title=title, ctime=ctime, href=href, city=city, )
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item

    def parse_item(self, response):
        item = response.meta['meta']
        article = response.xpath('//div[@class="con"]')
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attach = response.xpath('//div[@id="attach"]')
        attachments = attach.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)

        item.update(content=content, attachments=attachments_dict, )
        # print(item)
        yield item
