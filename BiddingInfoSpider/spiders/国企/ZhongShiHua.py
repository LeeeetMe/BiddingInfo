from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from scrapy import FormRequest


class ZhongShiHua(BaseSpider):
    name = 'ZhongShiHua'
    allowed_domains = ['bidding.sinopec.com']
    start_urls = []
    website_name = '中国石化电子招标投标交易平台'
    tmpl_url = "https://bidding.sinopec.com/tpfront/(S(iiigcylrvbvxl4x3smn4yp5g))/CommonPages/searchmore.aspx?CategoryNum=004001"

    def __init__(self, *a, **kw):
        super(ZhongShiHua, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 5

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                "MoreinfoListsearch1$Pager_input": str(i)
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data)
            yield request

    def parse_page(self, response):
        res = scrapy.Selector(response)
        li = res.xpath('//div[@class="titlecss"]')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath(".//a")
            title = a.xpath('.//@title').get()
            href = response.urljoin(a.xpath('.//@href').get())
            ctime = self.get_ctime(l.xpath('../following-sibling::td[1]//text()'))
            item.update(
                title=title,
                href=href,
                ctime=ctime,
            )
            # print(item)
            yield item
