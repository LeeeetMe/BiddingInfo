from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest


class BiLianWang(BaseSpider):
    name = 'BL'
    allowed_domains = ['ss.ebnew.com/']
    start_urls = ['http://ss.ebnew.com/tradingSearch/index.htm']
    website_name = '必联网'
    tmpl_url = 'http://ss.ebnew.com/tradingSearch/index.htm'
    endPageNum = 1

    def __init__(self, *a, **kw):
        super(BiLianWang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                'infoClassCodes': 'zbgg',
                'rangeType': '2',
                'projectType': 'bid',
                'pubDateType': 'today',
                'sortMethod': 'timeDesc',
                'currentPage': str(i),
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True)
            yield request

    def parse_page(self, response):
        li_lst = response.xpath('//div[@class="abstract-box mg-t25 ebnew-border-bottom mg-r15"]')
        for l in li_lst:
            item = BiddinginfospiderItem()
            a = l.xpath('.//a')

            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(l.xpath('.//i[2]//text()'))
            city = l.xpath(
                './/div[@class="abstract-content-items fl pd-l15 pd-t20 pd-b20 width-50"][2]//p[2]//span[2]//text()').extract_first()
            item.update(
                title=title,
                ctime=ctime,
                href=href,
                city=city,
            )
            yield item
            # yield scrapy.Request(
            #     url=href,
            #     dont_filter=True,
            #     callback=self.parse_item,
            #     meta={"dynamic": True, "xpath": '//div[@id="notLogin"]', 'item': item})

    def parse_item(self, response):
        item = response.meta.get("item")
        print(response.url)
        article = response.xpath('//div[@id="notLogin"]//tr|//div[@id="notLogin"]//p')
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
        industry = response.xpath('//span[@class="item-value"]//text()').extract()[-1]
        if industry:
            industry = industry.replace(";", "")

        item.update(
            content=content,
            attachments=attachments_dict,
            industry=industry
        )
        # print(item)
        yield item
