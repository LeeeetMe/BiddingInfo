import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class JiNan(BaseSpider):
    name = 'jinan'
    allowed_domains = ['http://jnggzy.jinan.gov.cn']
    start_urls = ['http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=0&xuanxiang=1&area=']
    website_name = '济南招投标'
    tmpl_url = 'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(JiNan, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 50

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                'xuanxiang': '招标公告',
                'pagenum': str(i),
                'type': '0',
                'subheading': '',
                'area': ''
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True, )
            yield request

    def parse_page(self, response):
        rs = json.loads(response.body.decode('utf8'))
        rs = rs['params'].get("str", False)
        selector = Selector(text=rs)
        alist = selector.xpath('//a')

        for a in alist:
            item = BiddinginfospiderItem()
            item['href'] = 'http://jnggzy.jinan.gov.cn/jnggzyztb/front/showNotice.do?iid=' + a.xpath(
                './/@onclick').extract_first()[9:-1] + '&xuanxiang=招标公告'
            item['title'] = a.xpath(".//text()").extract_first().strip()
            item['ctime'] = a.xpath('..//..//span[@class="span2"]//text()').extract_first()
            item['city'] = '济南'

            yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })

    def parse_item(self, response):
        item = response.meta['meta']
        # 主体
        main = response.xpath('//table[@align="center"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments
        print(item)
