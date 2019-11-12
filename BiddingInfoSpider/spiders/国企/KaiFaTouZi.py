import json

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class KaiFaTouZi(BaseSpider):
    name = 'KaiFaTouZi'
    allowed_domains = ['epp.ctg.com.cn']
    start_urls = ['http://eps.sdic.com.cn/gggc/index.jhtml']
    website_name = '国家开发投资公司电子采购平台'
    tmpl_url = 'http://eps.sdic.com.cn/gggc/index_{0}.jhtml'
    category = ""
    industry = ""

    def __init__(self, *a, **kw):
        super(KaiFaTouZi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = [self.tmpl_url.format(i) for i in range(1, 4)]

    def parse_start_url(self, response):
        li = response.xpath('//div[@class="lb-link"]/ul//li')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')
            title = a.xpath("@title").get()
            href = a.xpath("@href").get()
            ctime = self.get_ctime(l.xpath('.//span[@class="bidDate"]//text()'))

            item.update(
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            # print(item)
            yield item
