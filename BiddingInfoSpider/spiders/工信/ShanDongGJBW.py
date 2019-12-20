import json
import scrapy
from lxml import etree
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ShanDongGJBW(BaseSpider):
    name = 'ShanDongGJBW'
    allowed_domains = ['gxt.shandong.gov.cn']
    start_urls = ['http://gxt.shandong.gov.cn/col/col15177/index.html']
    website_name = '山东省工业和信息化-国家部委'
    tmpl_url = 'http://ggzyjyzx.shandong.gov.cn/module/web/jpage/dataproxy.jsp?page={0}&webid=78&path=http://gxt.shandong.gov.cn/&columnid=15177&unitid=71078&webname=%25E5%25B1%25B1%25E4%25B8%259C%25E7%259C%2581%25E5%25B7%25A5%25E4%25B8%259A%25E5%2592%258C%25E4%25BF%25A1%25E6%2581%25AF%25E5%258C%2596%25E5%258E%2585&permissiontype=0'

    def parse_start_url(self, response):
        datastore = response.xpath('//script[@type="text/xml"]/text()').get()
        # selector = etree.XML(response.body)
        if datastore:
            selector = etree.XML(datastore)
            a = selector.xpath('//nextgroup/text()')[0]
            href = etree.HTML(a).xpath('//a/@href')[0]
            req = self.make_requests_from_url(response.urljoin(href))
            req.callback = self.parse_shangdong_xml
            yield req

    def parse_shangdong_xml(self, response):
        # response已经完成返回xml的解析
        # datastore = etree.XML(response.text)
        html = ''.join(response.xpath('//record/text()').extract())

        # 产生内容页的请求
        for li in etree.HTML(html).xpath('//li'):
            item = BiddinginfospiderItem()
            a = li.xpath(".//a")[0]
            item['href'] = a.xpath(".//@href")[0]
            item['title'] = a.xpath(".//text()")[0]
            item['ctime'] = li.xpath('.//span//text()')[0]
            # print(item)
            yield item
        # 如果是全部爬取则继续获取下一页
        if not self.biddingInfo_update:
            selector = etree.XML(response.body)
            a = [0]
            next_select = selector.xpath('//nextgroup/text()')
            if next_select:
                a = next_select[0]
                href = etree.HTML(a).xpath('//a/@href')[0]
                req = self.make_requests_from_url(response.urljoin(href))
                req.callback = self.parse_shangdong_xml
                yield req


class ShanDongSWZF(ShanDongGJBW):
    name = 'ShanDongSWZF'
    start_urls = ['http://gxt.shandong.gov.cn/col/col15178/index.html']
    website_name = '山东省工业和信息化-省委政府'


class ShanDongBT(ShanDongGJBW):
    name = 'ShanDongBT'
    start_urls = ['http://gxt.shandong.gov.cn/col/col15178/index.html']
    website_name = '山东省工业和信息化-本厅'
