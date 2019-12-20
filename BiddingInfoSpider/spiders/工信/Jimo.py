from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class JiMo(BaseSpider):
    name = 'JiMo'
    allowed_domains = ['www.jimo.gov.cn']
    start_urls = ['http://www.jimo.gov.cn/n28356051/n6162/n6169/index.html']
    website_name = '即墨工信'
    tmpl_url = 'http://www.jimo.gov.cn/n28356051/n6162/n6169/index_{0}.html'

    def __init__(self, *a, **kw):
        super(JiMo, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls.extend([self.tmpl_url.format(i) for i in range(2, 18)])

    def parse_start_url(self, response):
        # print('reponse_request_url= ', response.request.url)
        li = response.xpath('//div[@id="listChangeDiv"]//li')
        for line in li:
            item = BiddinginfospiderItem()
            a = line.xpath('.//a')
            item['href'] = response.urljoin(a.xpath('@href').get())
            item['title'] = a.xpath('@title').get()
            item['ctime'] = line.xpath(".//span/text()").get()
            # print(item)
            yield item
