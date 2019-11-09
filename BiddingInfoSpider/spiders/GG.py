from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest
import json


class GG(BaseSpider):
    name = 'GG'
    allowed_domains = ['ss.ebnew.com/']
    start_urls = ['http://ss.ebnew.com/tradingSearch/index.htm']
    website_name = '必联网'
    tmpl_url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'
    endPageNum = 1

    def __init__(self, *a, **kw):
        super(GG, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                "TIMEBEGIN_SHOW": "2019-10-30",
                "TIMEEND_SHOW": "2019-11-08",
                "TIMEBEGIN": "2019-10-30",
                "TIMEEND": "2019-11-08",
                "SOURCE_TYPE": "1",
                "DEAL_TIME": "01",
                "DEAL_CLASSIFY": "00",
                "DEAL_STAGE": "0000",
                "DEAL_PROVINCE": "0",
                "DEAL_CITY": "0",
                "DEAL_PLATFORM": "0",
                "BID_PLATFORM": "0",
                "DEAL_TRADE": "0",
                "isShowAll": "1",
                "PAGENUMBER": "2",
                "FINDTXT": "",
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True)
            yield request

    def parse_page(self, response):
        print('request_url= ', response.request.url)
        body = json.loads(str(response.body, "utf-8"))
        li = body.get("data")
        for l in li:
            item = BiddinginfospiderItem()
            sheng = l.get('districtShow')
            shi = l.get('platformName').split("市")[0]
            href = l.get("url"),
            if isinstance(href, tuple):
                href = href[0]
            print("href is,", href)
            href = href.replace("a", "b")
            item.update(
                city=sheng + "-" + shi,
                title=l.get("title"),
                ctime=l.get("timeShow"),
                category=l.get("classifyShow"),
                href=href,
                industry=l.get("tradeShow"),
            )
            yield scrapy.Request(headers={
                "Referer": href},
                url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta.get("item")
        print(response.url)
        print(response.body.decode("utf-8"))
        article = response.xpath('//div[@id="mycontent"]')
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
        industry = response.xpath('//span[@class="item-value"]//text()').extract()[-1]
        if industry:
            industry = industry.replace(";", "")

        item.update(
            content=content,
            attachments=attachments_dict,
            industry=industry
        )
        print(item)
        # yield item
