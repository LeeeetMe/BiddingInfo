import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class AnHui(BaseSpider):
    name = 'anhui'
    allowed_domains = ['ggzy.ah.gov.cn']
    start_urls = ['http://ggzy.ah.gov.cn/login.do?method=beginlogin']
    website_name = '安徽公共资源交易'
    tmpl_url = 'http://ggzy.ah.gov.cn/dwr/call/plaincall/bulletinInfoDWR.getPackListForDwr1.dwr'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(AnHui, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'callCount': '1',
                'page': '/bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1',
                # 'httpSessionId': 'f95162dfd85a4fad4d374f5faf8c',
                # 'scriptSessionId': '5ECB85B67F8CC90DD5F6006267537EDD345',
                'c0-scriptName': 'bulletinInfoDWR',
                'c0-methodName': 'getPackListForDwr1',
                'c0-id': '0',
                'c0-e1': 'string:1',
                'c0-e2': 'string:',
                'c0-e3': 'string:jy',
                'c0-e4': 'string:1',
                'c0-e5': 'string:',
                'c0-e6': 'string:',
                'c0-e7': 'string:',
                'c0-e8': 'number:1',
                'c0-e9': 'string:10',
                'c0-e10': 'string:true',
                'c0-e11': 'string:packTable',
                'c0-param0': 'Object_Object:{id:reference:c0-e1,hySort:reference:c0-e2,bulletinclass:reference:c0-e3,fileType:reference:c0-e4,bulletinType:reference:c0-e5,district:reference:c0-e6,srcdistrict:reference:c0-e7,currentPage:reference:c0-e8,pageSize:reference:c0-e9,isPage:reference:c0-e10,tabId:reference:c0-e11}',
                'batchId': '8'
            }


        yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page, method='POST',
                             body=json.dumps(form_data))
        # request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True,)
        # yield request

    def parse_page(self, response):
        rs = response.body
        print('#######', rs)
        return
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
        item['title'] = main.xpath('//table[@class="header-table"]//tr[2]//td[2]//text()').extract_first()[2:]
        print(item)
