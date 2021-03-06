import requests

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest


class YiDongDianZi(BaseSpider):
    name = 'YiDongDianZi'
    allowed_domains = ['bidding.sinopec.com']
    start_urls = ['https://b2b.10086.cn/b2b/main/preIndex.html']
    website_name = '中国移动电子采购与招标投标系统'
    tmpl_url = 'https://b2b.10086.cn/b2b/main/showBiao!showZhaobiaoResult.html'
    endPageNum = 2
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "122",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "saplb_*=(J2EE204289720)204289752; JSESSIONID=0n4SKCHPKByVhhMLhVGvmOaZM3lZbgHYNi0M_SAPvqbC7Pbnqkvq23R4dnMX-j7J",
        "Host": "b2b.10086.cn",
        "Origin": "https://b2b.10086.cn",
        "Referer": "https://b2b.10086.cn/b2b/main/showBiao!preShowBiao.html?noticeType=list1",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self, *a, **kw):
        super(YiDongDianZi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 5

    def parse(self, response):
        for i in range(1, self.endPageNum):
            form_data = {
                "page.currentPage": str(i),
                "page.perPageSize": "20",
                "noticeBean.companyName": "",
                "noticeBean.title": "",
                "noticeBean.startDate": "",
                "noticeBean.endDate": "",

            }
            response = requests.post(self.tmpl_url, headers=self.headers, data=form_data)
            res = scrapy.Selector(text=response.text)
            li = res.xpath('//table[@class="jtgs_table"]//tr')
            article_tmp_url = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={0}'
            for l in li[1:]:
                item = BiddinginfospiderItem()
                a = l.xpath(".//a")
                id = l.xpath('@onclick').get()[14:-2]
                href = article_tmp_url.format(id)

                title = a.xpath('.//text()').get()
                item.update(
                    title=title,
                    href=href,
                )
                yield item
