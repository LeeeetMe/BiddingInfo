from urllib.parse import urljoin

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
from lxml import etree
from scrapy.selector import Selector


class QingDaoKX(BaseSpider):
    name = 'QingDaoKX'
    allowed_domains = ['qdstc.qingdao.gov.cn']
    start_urls = ['http://qdstc.qingdao.gov.cn/n32206674/n32206700/index.html']
    website_name = '青岛市科学技术局-政策法规-青岛市科技创新政策'
    tmpl_url = 'http://qdstc.qingdao.gov.cn/n32206674/n32206700/index_{0}.html'
    endPage = 12

    def __init__(self, *a, **kw):
        super(QingDaoKX, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls.extend([self.tmpl_url.format(i) for i in range(2, 12)])

    def parse_start_url(self, response):
        a_list = response.xpath('//div[@id="listChangeDiv"]//td//a')
        for a in a_list:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a.xpath('@href').get())
            item['ctime'] = a.xpath('../../td[3]//text()').get()
            item['title'] = a.xpath("@title").get()
            # print(item)
            yield item


class QingDaoKJDT(BaseSpider):
    name = 'QingDaoKJDT'
    allowed_domains = ['qdstc.qingdao.gov.cn']
    start_urls = ['http://qdstc.qingdao.gov.cn/n32206675/n32206705/index.html']
    website_name = '青岛市科学技术局- 科技动态'
    tmpl_url = 'http://27.223.1.61:8090/GetDynamicPager.ashx?templateGuid=160622143333175133&lkocok_pageNo={0}'
    endPage = 131

    def __init__(self, *a, **kw):
        super(QingDaoKJDT, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, self.endPage)])

    def parse_start_url(self, response):
        res = Selector(text=response.text[11:-2])
        a_list = res.xpath('//a')
        for a in a_list:
            item = BiddinginfospiderItem()
            item['href'] = urljoin("http://qdstc.qingdao.gov.cn", a.xpath('@href').get())
            item['ctime'] = a.xpath('../../td[3]//text()').get()
            item['title'] = a.xpath("@title").get()
            # print(item)
            yield item
