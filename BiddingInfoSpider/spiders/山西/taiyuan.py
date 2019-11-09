from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest
import json


class TaiYuan_ShiGong(BaseSpider):
    name = 'TaiYuan_ShiGong'
    allowed_domains = ['ggzyjy.zgzhijiang.gov.cn']
    start_urls = ['http://zjw.taiyuan.gov.cn/ggfw/bmfwcxl/zbgg/sg/index.shtml']
    website_name = '太原市住房和城乡建设局网站'
    tmpl_url = 'http://zjw.taiyuan.gov.cn/ggfw/bmfwcxl/zbgg/sg/index_{0}.shtml'
    city = "山西-太原"
    category = "工程建设"
    industry = "施工"
    endPage = 3

    def __init__(self, *a, **kw):
        super(TaiYuan_ShiGong, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls.extend([self.tmpl_url.format(i) for i in range(2, self.endPage)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//div[@class="list_service"]//tr')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')
            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(l.xpath(".//td[2]//text()"))
            item.update(
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})
            yield item
