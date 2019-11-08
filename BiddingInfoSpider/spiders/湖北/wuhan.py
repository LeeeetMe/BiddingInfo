import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class WuHan(BaseSpider):
    name = 'wuhan'
    allowed_domains = ['www.whzbtb.com']
    start_urls = ['https://www.whzbtb.com/V2PRTS/']
    website_name = '武汉公共资源交易'
    tmpl_url = 'https://www.whzbtb.com/V2PRTS/TendererNoticeInfoList.do'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(WuHan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 30

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'page': str(i),
                'rows': '10',
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True,meta={"dynamic": True,} )
            yield request

    def parse_page(self, response):
        rs = response.body
        selector = Selector(text=rs)
        alist = json.loads(selector.xpath('//body//text()').extract_first().strip())['rows']

        for a in alist:
            item = BiddinginfospiderItem()

            item['href'] = 'https://www.whzbtb.com/V2PRTS/TendererNoticeInfoDetail.do?id=' + a['id']
            # item['title'] = a['tenderPrjName'].encode("latin1").decode("gbk")
            item['ctime'] = a['updateDate'][0:10]
            item['city'] = '武汉'
            yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@class="pageRight_box"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments
        item['title']=main.xpath('//table[@class="header-table"]//tr[2]//td[2]//text()').extract_first()[2:]
        print(item)
