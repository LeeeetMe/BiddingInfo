import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class AnYang(BaseSpider):
    name = 'anyang'
    allowed_domains = ['www.ayggzy.cn/']
    start_urls = ['http://www.ayggzy.cn/jyxx/jsgcZbgg']
    website_name = '安阳公共资源交易'
    tmpl_url = 'http://www.ayggzy.cn/jyxx/jsgcZbgg'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(AnYang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 3

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                "currentPage": str(i),
                "area": '004',
                "secondArea": '000',
                "industriesTypeCode": '000',
                "city": "",
                "tenderProjectCode": "",
                "bulletinName": ""
            }
            # formdata
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True, )

            # payload
            # request = scrapy.Request(self.tmpl_url, callback=self.parse_page, method="POST", body=json.dumps(form_data),
            #                          dont_filter=True)
            yield request

    def parse_page(self, response):
        # a标签
        a = response.xpath('//table[@id="p2"]//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//@title").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//td[4]//text()').extract_first()
            item['city'] = '安阳'
            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@class="content_all_nr"]//span//p')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            '..//a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        # print(item)
        yield item
