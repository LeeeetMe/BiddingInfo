from datetime import date

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class NanShuiBeiDiao(BaseSpider):
    name = 'NanShuiBeiDiao'
    allowed_domains = ['cse-bidding.com']
    start_urls = [
        'http://zbcg.nsbd.cn/stoncms/category/belletinList.html?searchDate=1994-11-11&dates=300&word=&categoryId=88']
    website_name = '南水北调中线干线工程建设管理局招标采购交易平台'
    tmpl_url = 'http://www.cse-bidding.com/zgbqcms/category/belletinList.html?searchDate={0}&dates=300&categoryId=88&page={1}'
    category = ""
    industry = ""
    today = (date.today()).strftime("%Y-%m-%d")

    def __init__(self, *a, **kw):
        super(NanShuiBeiDiao, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(self.today, i) for i in range(1, 2)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//ul[@class="newslist"]//a')
        for a in li:
            item = BiddinginfospiderItem()
            title = a.xpath("..//h1").xpath('normalize-space(string(.))').get()
            href = a.xpath('.//@href').get()
            code = a.xpath('.//ul[@class="newsinfo"]//li[1]//span//text()').get()
            t = a.xpath('.//div[@class="newsDate"]').xpath('normalize-space(string(.))').get()

            if t:
                t = t.replace(" ", "").replace("/", "-")
            ctime = t[:3] + "-" + t[4:]

            item.update(
                code=code,
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            print(item)
            # yield item
