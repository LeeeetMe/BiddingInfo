from datetime import date

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class DianLiSheBei(BaseSpider):
    name = 'DianLiSheBei'
    allowed_domains = ['cse-bidding.com']
    start_urls = [
        'https://www.dlzb.com/gongcheng/gongcheng-1.html']
    website_name = '中国电力设备信息网电子招标交易平台'
    tmpl_url = 'https://www.dlzb.com/gongcheng/gongcheng-{0}.html'
    category = ""
    industry = ""
    today = (date.today()).strftime("%Y-%m-%d")

    def __init__(self, *a, **kw):
        super(DianLiSheBei, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(self.today, i) for i in range(1, 10)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//a[@class="gccon_title"]')
        print(li.getall())
        for a in li:
            item = BiddinginfospiderItem()
            title = a.xpath('normalize-space(string(.))').get()
            href = a.xpath('.//@href').get()
            t = a.xpath('../span[@class="gc_date"]').xpath('normalize-space(string(.))')
            ctime = self.get_ctime(t)

            item.update(
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            print(item)
            # yield item
