import json
import scrapy
from scrapy import FormRequest
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class HeBei(BaseSpider):
    name = 'hebei'
    allowed_domains = ['121.28.195.124:9001']
    start_urls = ['http://121.28.195.124:9001/tender/xxgk/list.do?selectype=zbgg#']
    website_name = '河北公共服务'
    tmpl_url = 'http://121.28.195.124:9001/tender/xxgk/zbgg.do'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(HeBei, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2

    def start_requests(self):
        for i in range(self.pageIndex):
            form_data = {
                'KeyType': 'ggname',
                'page': str(i),
                'KeyStr': '',
                'allDq': 'reset2',
                'allHy': 'reset1',
                'TimeStr': '',
                'AllPtName': ''
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True, )
            yield request

    def parse_page(self, response):
        a = response.xpath('//div[@class="publicont"]//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//text()").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//span//text()').extract_first()
            item['city'] = a1.xpath('..//..//..//p//span[2]//text()').extract_first()

            yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//table[@class="infro_table"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments
        print(item)
