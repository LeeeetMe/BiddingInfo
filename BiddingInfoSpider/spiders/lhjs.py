from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest


class EcpSgcc(BaseSpider):
    name = 'lhjs'
    allowed_domains = ['lhjs.cn']
    start_urls = ['https://www.lhjs.cn/BidNotice/jsgc/zbgg?Length=7&pageIndex=1']
    website_name = '漯河市公共资源交易信息网-建设工程'
    tmpl_url = 'https://www.lhjs.cn/BidNotice/jsgc/zbgg?Length=7'
    article_tmp = "https://www.lhjs.cn/BidNotice/jsgc/zbgg?Length=7&pageIndex={0}"
    item = ""
    """
    0  不限
    1  一天内
    2  三天内
    3  一周内
    4  一月内
    5  三月内
    """
    time_interval = "4"

    def __init__(self, *a, **kw):
        super(EcpSgcc, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 4)])

    def start_requests(self):
        for url in self.start_urls:
            form_data = {
                'time': self.time_interval,
                'area': "411100"
            }
            request = FormRequest(url, callback=self.parse_page, formdata=form_data)
            yield request

    def parse_page(self, response):
        li_lst = response.xpath('//div[@class="filter-content"]/ul/li')
        for l in li_lst:
            item = BiddinginfospiderItem()
            a = l.xpath('./a')
            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(a.xpath('.//span[@class="time"]//text()'))
            item.update(
                title=title,
                ctime=ctime,
                href=href,
            )
            yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta.get('item')
        print(response.url)
        article = response.xpath('//div[@id="TabContent"]//p')
        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attachments = article.xpath(
            './/a[contains(@href,".pdf") \
            or contains(@href,".rar") \
            or contains(@href,".doc") \
            or contains(@href,".xls") \
            or contains(@href,".zip") \
            or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)
        item.update(
            content=content,
            attachments=attachments_dict
        )
        print(item)
        yield item