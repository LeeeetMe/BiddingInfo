from datetime import date

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class HangKongGongYe(BaseSpider):
    name = 'HangKongGongYe'
    allowed_domains = ['ebid.eavic.com']
    start_urls = [
        'http://ebid.eavic.com/cms/channel/ywgg1hw/index.htm?pageNo=1']
    website_name = '航空工业电子采购平台电子招投标专区'
    tmpl_url = 'http://ebid.eavic.com/cms/channel/ywgg1hw/index.htm?pageNo={0}'
    category = ""
    industry = ""

    def __init__(self, *a, **kw):
        super(HangKongGongYe, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 22)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//li[@name="li_name"]//a')
        for a in li:
            item = BiddinginfospiderItem()
            title = a.xpath('@title').get()
            href = response.urljoin(a.xpath('.//@href').get())
            ctime = self.get_ctime(a.xpath('.//em[1]//text()'))
            item.update(
                ctime=ctime,
                industry=self.industry,
                category=self.category,
                title=title,
                href=href,
            )
            print(item)
            # yield item
