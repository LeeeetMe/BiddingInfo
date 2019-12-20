from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class QingDao(BaseSpider):
    name = 'QingDao'
    allowed_domains = ['qdeic.qingdao.gov.cn']
    start_urls = ['http://qdeic.qingdao.gov.cn/n28356049/n32561447/index.html']
    website_name = '青岛市工业和信息化局'
    tmpl_url = 'http://qdeic.qingdao.gov.cn/n28356049/n32561447/index_{0}.html'

    def __init__(self, *a, **kw):
        super(QingDao, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls.extend([self.tmpl_url.format(i) for i in range(2, 6)])

    def parse_start_url(self, response):
        print('reponse_request_url= ', response.request.url)
        li = response.xpath('//div[@id="listChangeDiv"]//li')
        for line in li:
            item = BiddinginfospiderItem()
            a = line.xpath('.//a')
            item['href'] = response.urljoin(a.xpath('@href').get())
            item['title'] = a.xpath('@title').get()
            item['ctime'] = line.xpath(".//span/text()").get()
            yield item
