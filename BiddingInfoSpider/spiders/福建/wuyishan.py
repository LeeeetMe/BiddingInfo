import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class WuYiShan(BaseSpider):
    name = 'wuyishan'
    allowed_domains = ['www.wysggzy.cn:81']
    start_urls = ['http://www.wysggzy.cn:81/hyweb/wysebid/wysIndex.do#']
    website_name = '武夷山公共资源交易'
    tmpl_url = 'http://www.wysggzy.cn:81/hyweb/transInfo/getTenderInfoPage.do'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(WuYiShan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 5

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                "tradeCode": 'WYSPT',
                "pageIndex": str(i),
                "pageSize": '10',
                "noticeTitle": '',
                "regionCode": '',
                "tenderType": "A",
                "pubTime": "",
                "state": "",
                "noticeType": "1"
            }
            # formdata
            # request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True, )

            # payload
            request = scrapy.Request(self.tmpl_url, callback=self.parse_page, method="POST", body=json.dumps(form_data),
                                     dont_filter=True)
            yield request

    def parse_page(self, response):

        rs = json.loads(response.body.decode('utf8'))
        rs = rs['data'].get("datalist", False)

        for a in rs:
            item = BiddinginfospiderItem()
            item[
                'href'] = 'http://www.wysggzy.cn:81/hyweb/wysebid/bidDetails.do?handle=1&tenderProjCode={0}&noticeType=1&flag=1&tenderProjId={1}&proj_id={2}&pre_evaId=&evaId={3}&signUpType={4}'.format(
                a['tenderProjCode'], a['tenderProjId'], a['proj_id'], a['evaId'], a['signUpType'])
            item['title'] = a['noticeTitle']
            item['ctime'] = a['sendTime']
            item['city'] = '武夷山'

            data = {"tenderProjCode": a['tenderProjCode'], "noticeType": "1", "noticeId": ""}

            # yield scrapy.Request(url='http://www.wysggzy.cn:81/hyweb/transInfo/getProjBuildNoticeById.do',
            #                      dont_filter=True, callback=self.parse_item, method="POST", body=json.dumps(data),
            #                      meta={'meta': item, })
            yield item

    # def parse_item(self, response):
    #     item = response.meta['meta']
    #     rs = json.loads(response.body.decode('utf8'))['data']["noticeList"][0]['content']
    #     selector = Selector(text=rs)
    #     # 主体
    #     main = selector.xpath('//p')
    #     # 正文
    #     item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
    #     # 附件
    #     attach = main.xpath(
    #         './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
    #     attachments = self.get_attachment(attach, response.request.url)
    #     item['attachments'] = attachments
    #     print(item)
