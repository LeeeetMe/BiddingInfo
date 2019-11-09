import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class QingHai(BaseSpider):
    name = 'qinghai'
    allowed_domains = ['qhggzyjy.gov.cn']
    start_urls = ['http://www.qhggzyjy.gov.cn/ggzy/jyxx/001001/001001001/secondPage.html']
    website_name = '青海省公共资源交易'
    tmpl_url = 'http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
    pageIndex = 0
    categ='工程建设'

    def __init__(self, *a, **kw):
        super(QingHai, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 1000

    def start_requests(self):
        for i in range(0, self.pageIndex,10):
            form_data = {"token": "", "pn": i, "rn": 10, "sdt": "", "edt": "", "wd": "", "inc_wd": "", "exc_wd": "",
                         "fields": "title", "cnum": "001;002;003;004;005;006;007;008;009;010",
                         "sort": "{\"showdate\":\"0\"}", "ssort": "title", "cl": 200, "terminal": "", "condition": [
                    {"fieldName": "categorynum", "isLike": True, "likeType": 2, "equal": "001001001"}], "time": None,
                         "highlights": "title", "statistics": None, "unionCondition": None, "accuracy": "100",
                         "noParticiple": "0", "searchRange": None, "isBusiness": 1}
            # request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True, )

            request = scrapy.Request(self.tmpl_url,
                                     callback=self.parse_page,
                                     method="POST",
                                     body=json.dumps(form_data),
                                     dont_filter=True)
            yield request

    def parse_page(self, response):
        rs = json.loads(response.body.decode('utf8'))
        rs = rs['result']['records']
        for a in rs:
            item = BiddinginfospiderItem()
            item['href'] =response.urljoin(a['linkurl'])
            item['title'] = a['title']
            item['ctime'] = a['showdate'][0:10]
            item['city'] = a['xiaquname']

            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield  item

    # def parse_item(self, response):
    #     item = response.meta['meta']
    #     # 主体
    #     main = response.xpath('//div[@class="ewb-ca-detail"]')
    #     # 正文
    #     item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
    #     # 附件
    #     attach = response.xpath('//p[@class="ewb-info-end"]')
    #     attach = attach.xpath(
    #         './/a[contains(text(),".pdf") or contains(text(),".rar") or contains(text(),".doc") or contains(text(),".xls") or contains(text(),".zip") or contains(text(),".docx")]')
    #     attachments = self.get_attachment(attach, response.request.url)
    #     item['attachments'] = attachments
    #     item['category'] = self.categ
    #     print(item)

