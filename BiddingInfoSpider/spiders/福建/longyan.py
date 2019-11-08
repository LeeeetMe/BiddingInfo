import json

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class LongYan(BaseSpider):
    name = 'LongYan_JianShe'
    allowed_domains = ['lyszb.com']
    start_urls = ['http://www.lyszb.com/hyweb/xlebid/index.do']
    website_name = '龙岩电子交易平台'
    tmpl_url = 'http://www.lyszb.com/hyweb/transInfo/getTenderInfoPage.do'
    category = "工程建设"
    endPageNum = 2
    headers = {
        # "Host": "www.lyszb.com",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        # "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        # "Accept-Encoding": " gzip, deflate",
        "Content-Type": "application/json;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://www.lyszb.com",
        # "Connection": "keep-alive",
        "Referer": "http://www.lyszb.com/hyweb/xlebid/index.do"
    }

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                "pageIndex": str(i),
                "pageSize": "10",
                "tradeCode": "XLHYZPT",
                # "noticeTitle": None,
                # "regionCode": None,
                "tenderType": "JY",
                # "transType": None,
                "pubTime": "day30",
                "state": "1",  # "" 全部、"0" 待开标 、"1" 已开标
                "noticeType": "1",
                "projentity": "1",
                # "tDeptid": None,
                # "Cookie": "JSESSIONID=DA81107C8237AC6D87DDF33DFA00776A; JSESSIONID=EFA50AB1FCB3DBEF5D4714EA17387D9E"
            }
            # payload
            request = scrapy.Request(self.tmpl_url,
                                     callback=self.parse_page,
                                     headers=self.headers,
                                     method="POST",
                                     body=json.dumps(form_data),
                                     dont_filter=True)
            yield request

    def parse_page(self, response):
        print('request_url= ', response.request.url)
        res = json.loads(str(response.body, encoding="utf-8"))
        data_list = res["data"]["datalist"]
        if data_list:
            tmp_href = 'http://www.lyszb.com/hyweb/hyebid/smallScaleProject.do?&tenderProjId={0}'
            for data in data_list:
                item = dict()
                print(data)
                title = data.get("proj_name")
                code = data.get("tenderSelfCode")
                ctime = data.get("sendTime")
                tenderProjId = data.get("tenderProjId")
                href = tmp_href.format(tenderProjId)
                item.update(
                    category=self.category,
                    title=title,
                    code=code,
                    ctime=ctime,
                    href=href,
                )
                yield scrapy.Request(url=href,
                                     dont_filter=True,
                                     callback=self.parse_item,
                                     meta={"item": item, "dynamic": True})

    def parse_item(self, response):
        item = response.meta["item"]
        print(response.url)
        article = response.xpath('//div[@id="main"]')
        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attachments_dict = dict()
        att_list = response.xpath('//ul[@id="attachArea"]//li//a')
        if att_list:
            for i in att_list:
                name = i.xpath('.//@title').extract_first()
                attr = i.xpath('//@onclick').extract_first()
                url = attr[15:-6]
                attachments_dict.update({name: url})

        item.update(
            content=content,
            attachments=attachments_dict
        )
        print(item)
        # yield item
