import json

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ShanDongKXJST(BaseSpider):
    name = 'ShanDongKXJST'
    allowed_domains = ['wwww.sdstc.gov.cn']
    start_urls = [
        'http://www.sdstc.gov.cn:81/news/1202/?data=%7B%22firstNavigation%22%3A%223bef7f41c58a4478b18510a32636bb4e%22%2C%22secondNavigation%22%3A%22ab57841fda904c53b9a258edf557baae%22%2C%22thirdNavigation%22%3A%2253d20d22471f4f3d998ba671d790696a%22%2C%22headSearch%22%3A%22%22%2C%22pageNo%22%3A1%2C%22pageSize%22%3A25%7D']
    website_name = '山东省科学技术厅-政策发布'
    tmpl_url = 'http://www.sdstc.gov.cn:81/news/1202/?data=%7B%22firstNavigation%22%3A%223bef7f41c58a4478b18510a32636bb4e%22%2C%22secondNavigation%22%3A%22ab57841fda904c53b9a258edf557baae%22%2C%22thirdNavigation%22%3A%2253d20d22471f4f3d998ba671d790696a%22%2C%22headSearch%22%3A%22%22%2C%22pageNo%22%3A1%2C%22pageSize%22%3a200%7d'

    def __init__(self, *a, **kw):
        super(ShanDongKXJST, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = [self.tmpl_url]

    def parse_start_url(self, response):
        data = json.loads(str(response.body, "utf-8"))
        data_list = data.get("dataList", [])
        for d in data_list:
            item = BiddinginfospiderItem()
            item['href'] = "http://www.sdstc.gov.cn/page/subpage/detail.html?id=" + d.get('id')
            item['title'] = d.get('title')
            item['ctime'] = d.get('updateTime')
            # print(item)
            yield item


class ShanDongKJZX(BaseSpider):
    name = "ShanDongKJZX"
    allowed_domains = ['http://www.sdstc.gov.cn']
    start_urls = [
        'http://www.sdstc.gov.cn:81/news/1202/?data=%7B%22firstNavigation%22%3A%22b26552d22b9644a8ad9ed25ccc4b9f79%22%2C%22secondNavigation%22%3A%22%22%2C%22pageNo%22%3A1%2C%22pageSize%22%3A%2225%22%7D']
    website_name = '山东省科学技术厅-科技资讯'
    tmpl_url = 'http://www.sdstc.gov.cn:81/news/1202/?data=%7B%22firstNavigation%22%3A%22b26552d22b9644a8ad9ed25ccc4b9f79%22%2C%22secondNavigation%22%3A%22%22%2C%22pageNo%22%3A{0}%2C%22pageSize%22%3A%221000%22%7D'

    def __init__(self, *a, **kw):
        super(ShanDongKJZX, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 8)])

    def parse_start_url(self, response):
        data = json.loads(str(response.body, "utf-8"))
        data_list = data.get("dataList", [])
        for d in data_list:
            item = BiddinginfospiderItem()
            item['href'] = "http://www.sdstc.gov.cn/page/subpage/detail.html?id=" + d.get('id')
            item['title'] = d.get('title')
            item['ctime'] = d.get('updateTime')
            # print(item)
            yield item
