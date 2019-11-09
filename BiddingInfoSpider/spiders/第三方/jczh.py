import scrapy
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class JingCaiZH(BaseSpider):
    name = 'jingcaizh'
    allowed_domains = ['www.jczh100.com']
    start_urls = ['http://www.jczh100.com/index/tendering/li.html?zhuanti=&et=&industry=&t=z&hangye=&so=&quyu=&gonggao=1&xinxi=&page=1#somap']
    website_name = '精彩纵横'
    tmpl_url = ['http://www.jczh100.com/index/tendering/li.html?zhuanti=&et=&industry=&t=z&hangye=&so=&quyu=&gonggao=1&xinxi=&page=%s#somap' % i for i in range(1, 100)]

    def __init__(self, *a, **kw):
        super(JingCaiZH, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        # a标签
        a = response.xpath('//ul[@class="pinfolist pinfolist01"]//a[@class="tit"]')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//span[2]//text()").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//..//div[@class="date fl"]//p[2]//text()').extract_first()[5:15]
            item['city'] =a1.xpath('..//..//div[1]//span[@class="ic01"][1]//text()').extract_first().strip()
            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item

    # def parse_item(self, response):
    #     item = response.meta['meta']
    #     # 主体
    #     main = response.xpath('//div[@class="con"]')
    #     # 正文
    #     item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
    #     # 附件
    #     attach = main.xpath(
    #         '..//a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
    #     attachments = self.get_attachment(attach, response.request.url)
    #     item['attachments'] = attachments
    #
    #     print(item)
