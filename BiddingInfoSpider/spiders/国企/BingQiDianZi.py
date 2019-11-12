from datetime import date

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class BingQiDianZi(BaseSpider):
    name = 'BingQiDianZi'
    allowed_domains = ['cse-bidding.com']
    start_urls = [
        'http://www.cse-bidding.com/zgbqcms/category/belletinList.html?searchDate=2019-10-11&dates=30&word=&categoryId=88']
    website_name = '中国兵器电子招标投标交易平台'
    tmpl_url = 'http://www.cse-bidding.com/zgbqcms/category/belletinList.html?searchDate={0}&dates=90&categoryId=88&page={1}'
    category = ""
    industry = ""
    today = (date.today()).strftime("%Y-%m-%d")

    def __init__(self, *a, **kw):
        super(BingQiDianZi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(self.today, i) for i in range(1, 5)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//ul[@class="newslist"]//a')
        print(li.getall())
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
            # print(item)
            yield item
