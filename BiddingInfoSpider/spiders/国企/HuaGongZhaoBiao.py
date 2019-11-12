from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class HuaGongZhaoBiao(BaseSpider):
    name = 'HuaGongZhaoBiao'
    allowed_domains = ['hgzbw.cn']
    start_urls = ['http://www.hgzbw.cn/l_chem-zhaobiao_1.html']
    website_name = '中国化工装备招投标交易平台'
    tmpl_url = 'http://www.hgzbw.cn/l_chem-zhaobiao_{0}.html'
    category = ""
    industry = ""

    def __init__(self, *a, **kw):
        super(HuaGongZhaoBiao, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 24)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//a[@class="pdlistc"]')
        for a in li:
            item = BiddinginfospiderItem()
            title = a.xpath('normalize-space(string(.))').get()
            href = response.urljoin(a.xpath('.//@href').get())
            ctime = self.get_ctime(a.xpath('../following-sibling::td[2]//text()'))
            city = a.xpath('../preceding-sibling::td[1]').xpath('normalize-space(string(.))').get()

            item.update(
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
                city=city,
            )
            # print(item)
            yield item
